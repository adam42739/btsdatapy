import pandas as pd
from btsdatapy.core.config import SETTINGS
from btsdatapy.core.models.config import BtsTableConfig
from btsdatapy.core.models.requests import BtsTableRequest
from btsdatapy.core.services.clients import BtsStatefulClient
from btsdatapy.core.utils.cache import is_cached, read_cache, write_cache


def _fetch_cached_table(table_id: str, user_parameters: dict[str, str]) -> pd.DataFrame:
    if not SETTINGS.cache_enabled:
        return pd.DataFrame()

    if not is_cached(user_parameters, table_id=table_id):
        return pd.DataFrame()

    return read_cache(user_parameters, table_id=table_id)


def _fetch_single_table(
    client: BtsStatefulClient,
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


def fetch_table(
    table_config: BtsTableConfig,
    columns: list[str],
    all_user_parameters: list[dict[str, str]],
) -> pd.DataFrame:
    client = BtsStatefulClient(table_config.get_url())

    dfs = []
    for user_parameters in all_user_parameters:
        df = _fetch_single_table(client, table_config, columns, user_parameters)

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
