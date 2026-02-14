import io
import zipfile

import pandas as pd
import requests
from bs4 import BeautifulSoup
from btsdatapy.core.cache import is_cached, read_cache, write_cache
from btsdatapy.core.config import LOOKUP_CONFIGS, SETTINGS
from btsdatapy.core.constants import BASE_URL, USER_AGENT
from btsdatapy.core.models.config import BtsLookupConfig, BtsLookupType, BtsTableConfig
from btsdatapy.core.models.request import BtsTableRequest


def _fetch_cached_lookup(lookup_config: BtsLookupConfig) -> pd.DataFrame:
    if not SETTINGS.cache_enabled:
        return pd.DataFrame()

    if not is_cached(lookup_id=lookup_config.lookup_id):
        return pd.DataFrame()

    return read_cache(lookup_id=lookup_config.lookup_id)


def _fetch_lookup(lookup_config: BtsLookupConfig) -> pd.DataFrame:
    cached_df = _fetch_cached_lookup(lookup_config)
    if not cached_df.empty:
        return cached_df

    resp = requests.get(lookup_config.get_url())
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text))
    df = df.rename(columns={"Code": "lookup_key", "Description": "lookup_value"})

    write_cache(df, lookup_id=lookup_config.lookup_id)

    return df


def get_lookup(lookup_config: BtsLookupConfig) -> pd.DataFrame:
    if lookup_config.type == BtsLookupType.FETCH:
        return _fetch_lookup(lookup_config)
    elif lookup_config.type == BtsLookupType.DATA:
        return pd.DataFrame(
            [
                {"lookup_key": key, "lookup_value": value}
                for key, value in lookup_config.mapping.items()
            ]
        )


def _extract_aspnet_value(soup: BeautifulSoup, name: str) -> str:
    return soup.find("input", {"name": name})["value"]


class BtsTableClient:
    def __init__(
        self,
        base_url: str,
        user_agent: str = USER_AGENT,
        referer: str = BASE_URL,
    ):
        self.base_url = base_url
        self.user_agent = user_agent
        self.referer = referer

        self._init_session()

    def _init_session(self):
        self.session = requests.Session()

        headers = {
            "User-Agent": self.user_agent,
            "Referer": self.referer,
        }
        resp = self.session.get(self.base_url, headers=headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        self.viewstate = _extract_aspnet_value(soup, "__VIEWSTATE")
        self.eventvalidation = _extract_aspnet_value(soup, "__EVENTVALIDATION")
        self.viewstategenerator = _extract_aspnet_value(soup, "__VIEWSTATEGENERATOR")

    def fetch_table(self, table_request: BtsTableRequest) -> pd.DataFrame:
        table_request.set_asp_state(
            self.viewstate, self.eventvalidation, self.viewstategenerator
        )

        url = table_request.get_url()
        payload = table_request.get_payload()
        headers = table_request.get_headers()

        resp = self.session.post(url, headers=headers, data=payload)
        resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            csv_content = z.read(z.namelist()[0]).decode("utf-8")

        df = pd.read_csv(io.StringIO(csv_content), dtype=str)
        df = df.rename(columns=table_request.table_config.get_column_name_mapping())

        return df


def _fetch_cached_table(table_id: str, user_parameters: dict[str, str]) -> pd.DataFrame:
    if not SETTINGS.cache_enabled:
        return pd.DataFrame()

    if not is_cached(user_parameters=user_parameters, table_id=table_id):
        return pd.DataFrame()

    return read_cache(user_parameters=user_parameters, table_id=table_id)


def _fetch_single_table(
    client: BtsTableClient,
    table_config: BtsTableConfig,
    columns: list[str],
    user_parameters: dict[str, str],
) -> pd.DataFrame:
    cached_df = _fetch_cached_table(table_config.table_id.value, user_parameters)

    columns_needed = list(set(columns) - set(cached_df.columns))
    if not columns_needed:
        return cached_df[columns]

    table_request = BtsTableRequest(
        table_config=table_config,
        columns=list(set(columns_needed) | set(table_config.primary_key)),
        user_parameters=user_parameters,
    )

    fetched_df = client.fetch_table(table_request)

    if cached_df.empty and fetched_df.empty:
        return pd.DataFrame(columns=columns)
    elif cached_df.empty:
        df = fetched_df
    elif fetched_df.empty:
        df = cached_df
    else:
        df = pd.merge(
            cached_df,
            fetched_df,
            how="outer",
            on=table_request.table_config.primary_key,
        )

    write_cache(
        df,
        table_request.user_parameters,
        table_id=table_request.table_config.table_id.value,
    )

    df = df[columns]

    return df


def _create_lookup_columns(
    table_config: BtsTableConfig, columns: list[str], df: pd.DataFrame
) -> pd.DataFrame:
    for col in columns:
        if not col.startswith("*"):
            continue

        column_config = next(
            column for column in table_config.columns if column.name == col[1:]
        )

        if not column_config.has_lookup:
            continue

        lookup_paths = column_config.lookup.split(".")
        lookup_config = LOOKUP_CONFIGS
        for path in lookup_paths:
            if path.startswith("l_"):
                lookup_config = lookup_config["lookups"][path]
            else:
                lookup_config = lookup_config[path]

        lookup_df = get_lookup(lookup_config)

        df = df.merge(lookup_df, left_on=col[1:], right_on="lookup_key", how="left")
        df = df.rename(columns={"lookup_value": col})

    return df


def fetch_table(
    table_config: BtsTableConfig,
    columns: list[str],
    all_user_parameters: list[dict[str, str]],
) -> pd.DataFrame:
    client = BtsTableClient(table_config.get_url())

    stripped_columns = list(
        set([col[1:] if col.startswith("*") else col for col in columns])
    )

    dfs = []
    for user_parameters in all_user_parameters:
        df = _fetch_single_table(
            client, table_config, stripped_columns, user_parameters
        )
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)

    df = _create_lookup_columns(table_config, columns, df)
    df = df[columns]

    return df
