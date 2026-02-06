import pandas as pd
from btsdatapy.core.models.requests import BtsTableRequest
from btsdatapy.core.services.clients import BtsStatefulClient


def fetch_table(
    table_request: BtsTableRequest, user_parameters: list[dict[str, str]]
) -> pd.DataFrame:
    client = BtsStatefulClient(table_request.get_url())

    dfs = []
    for params in user_parameters:
        table_request.set_user_parameters(params)
        df = client.fetch_table(table_request)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
