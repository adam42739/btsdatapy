import io
import zipfile
from unittest.mock import Mock, patch

import pandas as pd
from btsdatapy.core.clients import BtsStatefulClient, BtsStatelessClient
from btsdatapy.core.models.requests import BtsTableRequest, BtsTableRequestPayload


def _make_zip_bytes(csv_bytes: bytes) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("test_table.csv", csv_bytes)
    return buffer.getvalue()


TEST_HTML_WITH_ASP_NET_STATE = (
    '<input name="__VIEWSTATE" value="VS"/>'
    '<input name="__EVENTVALIDATION" value="EV"/>'
    '<input name="__VIEWSTATEGENERATOR" value="VG"/>'
)

TEST_DATAFRAME_DICT = {"col1": ["val1"], "col2": ["val2"]}
TEST_DATAFRAME = pd.DataFrame(TEST_DATAFRAME_DICT)
TEST_DATAFRAME_STRING = TEST_DATAFRAME.to_csv(index=False)
TEST_DATAFRAME_BYTES = TEST_DATAFRAME_STRING.encode("utf-8")
TEST_DATAFRAME_ZIP_BYTES = _make_zip_bytes(TEST_DATAFRAME_BYTES)

TEST_TABLE_ID = "test-id"
TEST_TABLE_NAME = "test-name"


def test_bts_stateful_client_fetch_table():
    get_resp = Mock()
    get_resp.text = TEST_HTML_WITH_ASP_NET_STATE
    get_resp.raise_for_status = Mock()

    post_resp = Mock()
    post_resp.content = TEST_DATAFRAME_ZIP_BYTES
    post_resp.raise_for_status = Mock()

    with patch("btsdatapy.core.clients.requests.Session") as MockSession:
        mock_session = MockSession.return_value
        mock_session.get.return_value = get_resp
        mock_session.post.return_value = post_resp

        client = BtsStatefulClient(base_url="http://example.com")

        table_request = BtsTableRequest(
            table_id=TEST_TABLE_ID,
            sh146_name=TEST_TABLE_NAME,
            payload=BtsTableRequestPayload(),
        )
        df = client.fetch_table(table_request)

        assert isinstance(df, pd.DataFrame)
        assert df.shape == TEST_DATAFRAME.shape
        assert df.to_dict("list") == TEST_DATAFRAME_DICT

        mock_session.get.assert_called()
        mock_session.post.assert_called()
        assert table_request.payload.VIEWSTATE == "VS"
        assert table_request.payload.EVENTVALIDATION == "EV"
        assert table_request.payload.VIEWSTATEGENERATOR == "VG"


def test_bts_stateless_client_fetch_lookup():
    lookup_request = Mock()
    lookup_request.get_url.return_value = "http://example.com/lookup.csv"

    get_resp = Mock()
    get_resp.text = TEST_DATAFRAME_STRING
    get_resp.raise_for_status = Mock()

    with patch(
        "btsdatapy.core.clients.requests.get", return_value=get_resp
    ) as mock_get:
        df = BtsStatelessClient.fetch_lookup(lookup_request)

        assert isinstance(df, pd.DataFrame)
        assert df.shape == TEST_DATAFRAME.shape
        assert df.to_dict("list") == TEST_DATAFRAME_DICT

        mock_get.assert_called_with(lookup_request.get_url())
