from enum import Enum

from btsdatapy.core.constants import (
    ASP_DOWNLOAD_LOOKUP,
    ASP_DOWNLOAD_TABLE,
    ASP_LOOKUP_PARAM,
    ASP_SH146_NAME_PARAM,
    ASP_TABLE_ID_PARAM,
    BASE_URL,
)
from btsdatapy.core.utils import rot13
from pydantic import BaseModel


class BtsTableId(BaseModel):
    value: str
    rot13: bool


class BtsSh146Name(BaseModel):
    value: str
    rot13: bool


class BtsPayloadFixedParameter(BaseModel):
    name: str
    value: str


class BtsPayloadUserParameter(BaseModel):
    name: str
    type: str


class BtsTableColumn(BaseModel):
    name: str
    payload_name: str
    response_name: str
    has_lookup: bool
    lookup: str | None = None


class BtsTableConfig(BaseModel):
    table_id: BtsTableId
    table_sh146_name: BtsSh146Name
    fixed_parameters: list[BtsPayloadFixedParameter]
    user_parameters: list[BtsPayloadUserParameter]
    primary_key: list[str]
    columns: list[BtsTableColumn]

    def get_column_name_mapping(self) -> dict[str, str]:
        return {col.response_name: col.name for col in self.columns}

    def get_url(self) -> str:
        table_id = (
            self.table_id.value
            if not self.table_id.rot13
            else rot13(self.table_id.value)
        )
        sh146_name = (
            self.table_sh146_name.value
            if not self.table_sh146_name.rot13
            else rot13(self.table_sh146_name.value)
        )
        return (
            f"{BASE_URL}{ASP_DOWNLOAD_TABLE}"
            f"{ASP_TABLE_ID_PARAM}={table_id}&"
            f"{ASP_SH146_NAME_PARAM}={sh146_name}"
        )


class BtsLookupType(Enum):
    FETCH = "fetch"
    DATA = "data"


class BtsLookupConfig(BaseModel):
    type: BtsLookupType
    name: str
    lookup_id: str | None = None
    rot13: bool | None = None
    mapping: dict[str, str] | None = None

    def get_url(self) -> str | None:
        if self.type != BtsLookupType.FETCH or not self.lookup_id:
            return None

        if self.rot13:
            lookup_param = f"{ASP_LOOKUP_PARAM}={rot13(self.lookup_id)}"
        else:
            lookup_param = f"{ASP_LOOKUP_PARAM}={self.lookup_id}"

        return f"{BASE_URL}{ASP_DOWNLOAD_LOOKUP}{lookup_param}"
