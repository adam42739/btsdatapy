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
    has_lookup: bool
    lookup: str | None = None


class BtsTableConfig(BaseModel):
    table_id: BtsTableId
    table_sh146_name: BtsSh146Name
    fixed_parameters: list[BtsPayloadFixedParameter]
    user_parameters: list[BtsPayloadUserParameter]
    columns: list[BtsTableColumn]


class BtsLookupConfig(BaseModel):
    type: str
    name: str
    lookup_id: str | None = None
    rot13: bool | None = None
    mapping: dict[str, str] | None = None
