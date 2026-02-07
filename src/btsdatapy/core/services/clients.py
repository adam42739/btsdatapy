import io
import zipfile

import pandas as pd
import requests
from bs4 import BeautifulSoup
from btsdatapy.core.constants import BASE_URL, USER_AGENT
from btsdatapy.core.models.requests import BtsLookupRequest, BtsTableRequest


def _extract_aspnet_value(soup: BeautifulSoup, name: str) -> str:
    return soup.find("input", {"name": name})["value"]


class BtsStatefulClient:
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


class BtsStatelessClient:
    @staticmethod
    def fetch_lookup(lookup: BtsLookupRequest) -> pd.DataFrame:
        resp = requests.get(lookup.get_url())
        resp.raise_for_status()
        return pd.read_csv(io.StringIO(resp.text))
