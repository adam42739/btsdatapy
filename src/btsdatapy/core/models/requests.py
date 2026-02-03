from dataclasses import dataclass
from enum import Enum
from typing import Any

from btsdatapy.core.constants import (
    ASP_DOWNLOAD_LOOKUP,
    ASP_DOWNLOAD_TABLE,
    ASP_LOOKUP_PARAM,
    ASP_SH146_NAME_PARAM,
    ASP_TABLE_ID_PARAM,
    BASE_URL,
    CONTENT_TYPE,
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
        return (
            f"{BASE_URL}{ASP_DOWNLOAD_TABLE}"
            f"{ASP_TABLE_ID_PARAM}={self.table_id}&"
            f"{ASP_SH146_NAME_PARAM}={self.sh146_name}"
        )

    def get_payload(self) -> dict[str, Any]:
        return self.payload.model_dump(by_alias=True, exclude_none=True)

    def get_headers(self) -> dict[str, Any]:
        self.headers.Referer = self.get_url()
        return self.headers.model_dump(by_alias=True)


class BtsLookupRequest(Enum):
    def get_url(self) -> str:
        return f"{BASE_URL}{ASP_DOWNLOAD_LOOKUP}{ASP_LOOKUP_PARAM}={self.value}"
