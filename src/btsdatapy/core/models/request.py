from btsdatapy.core.constants import BASE_URL, CONTENT_TYPE, USER_AGENT
from btsdatapy.core.models.config import BtsTableConfig


class BtsTableRequest:
    def __init__(
        self,
        table_config: BtsTableConfig,
        columns: list[str],
        user_parameters: dict[str, str],
    ):
        self._eventtarget: str = ""
        self._eventargument: str = ""
        self._lastfocus: str = ""
        self._viewstate: str = ""
        self._viewstategenerator: str = ""
        self._eventvalidation: str = ""

        self.table_config = table_config
        self.user_parameters = user_parameters
        self.columns = list(set(columns) | set(table_config.primary_key))

    def set_asp_state(
        self, viewstate: str, eventvalidation: str, viewstategenerator: str
    ):
        self._viewstate = viewstate
        self._eventvalidation = eventvalidation
        self._viewstategenerator = viewstategenerator

    def get_url(self) -> str:
        return self.table_config.get_url()

    def get_headers(self) -> dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Content-Type": CONTENT_TYPE,
            "Referer": self.get_url(),
            "Origin": BASE_URL,
        }

    def get_payload(self) -> dict[str, str]:
        payload = {
            "__EVENTTARGET": self._eventtarget,
            "__EVENTARGUMENT": self._eventargument,
            "__LASTFOCUS": self._lastfocus,
            "__VIEWSTATE": self._viewstate,
            "__VIEWSTATEGENERATOR": self._viewstategenerator,
            "__EVENTVALIDATION": self._eventvalidation,
        }

        for fixed_param in self.table_config.fixed_parameters:
            payload[fixed_param.name] = fixed_param.value

        for param, value in self.user_parameters.items():
            payload[param] = value

        for column in self.table_config.columns:
            if column.name in self.columns:
                payload[column.payload_name] = "on"

        return payload
