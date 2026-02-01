from dataclasses import dataclass
from typing import Any

from btsdatapy._core.constants import (
    BASE_URL,
    CONTENT_TYPE,
    DOWNLOAD_ASPX,
    SH146_NAME_PARAM,
    TABLE_ID_PARAM,
    USER_AGENT,
)
from pydantic import BaseModel, Field


class BtsTableRequestPayload(BaseModel):
    EVENTTARGET: str = Field("", alias="__EVENTTARGET")
    EVENTARGUMENT: str = Field("", alias="__EVENTARGUMENT")
    LASTFOCUS: str = Field("", alias="__LASTFOCUS")
    VIEWSTATE: str = Field("", alias="__VIEWSTATE")
    VIEWSTATEGENERATOR: str = Field("", alias="__VIEWSTATEGENERATOR")
    EVENTVALIDATION: str = Field("", alias="__EVENTVALIDATION")

    def set_aspnet_state(
        self, viewstate: str, eventvalidation: str, viewstategenerator: str
    ):
        self.VIEWSTATE = viewstate
        self.EVENTVALIDATION = eventvalidation
        self.VIEWSTATEGENERATOR = viewstategenerator


class BtsTableRequestHeaders(BaseModel):
    User_Agent: str = Field(USER_AGENT, alias="User-Agent")
    Content_Type: str = Field(CONTENT_TYPE, alias="Content-Type")
    Referer: str = ""
    Origin: str = BASE_URL


@dataclass
class BtsTableRequest:
    table_id: str
    sh146_name: str

    payload: BtsTableRequestPayload
    headers: BtsTableRequestHeaders = BtsTableRequestHeaders()

    def get_url(self) -> str:
        aspx_params = (
            f"{TABLE_ID_PARAM}={self.table_id}&{SH146_NAME_PARAM}={self.sh146_name}"
        )
        return f"{BASE_URL}{DOWNLOAD_ASPX}{aspx_params}"

    def get_payload(self) -> dict[str, Any]:
        return self.payload.model_dump(by_alias=True, exclude_none=True)

    def get_headers(self) -> dict[str, Any]:
        self.headers.Referer = self.get_url()
        return self.headers.model_dump(by_alias=True)
