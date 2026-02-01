import io
import zipfile
from unittest.mock import Mock, patch

import pandas as pd
from btsdatapy._core.clients import BtsAspNetClient
from btsdatapy._core.models import BtsTableRequest, BtsTableRequestPayload


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

TEST_DATAFRAME = pd.DataFrame({"a": [1], "b": [2]})
TEST_DATAFRAME_ZIP_BYTES = _make_zip_bytes(
    TEST_DATAFRAME.to_csv(index=False).encode("utf-8")
)

TEST_TABLE_ID = "test-id"
TEST_TABLE_NAME = "test-name"


def test_bts_asp_net_client_fetch_table():
    get_resp = Mock()
    get_resp.text = TEST_HTML_WITH_ASP_NET_STATE
    get_resp.raise_for_status = Mock()

    post_resp = Mock()
    post_resp.content = TEST_DATAFRAME_ZIP_BYTES
    post_resp.raise_for_status = Mock()

    with patch("btsdatapy._core.clients.requests.Session") as MockSession:
        mock_session = MockSession.return_value
        mock_session.get.return_value = get_resp
        mock_session.post.return_value = post_resp

        client = BtsAspNetClient(base_url="http://example.com")

        table = BtsTableRequest(
            table_id=TEST_TABLE_ID,
            sh146_name=TEST_TABLE_NAME,
            payload=BtsTableRequestPayload(),
        )
        df = client.fetch_table(table)

        assert isinstance(df, pd.DataFrame)
        assert df.shape == (1, 2)
        assert df.iloc[0].to_dict() == {"a": 1, "b": 2}

        mock_session.get.assert_called()
        mock_session.post.assert_called()
        assert table.payload.VIEWSTATE == "VS"
        assert table.payload.EVENTVALIDATION == "EV"
        assert table.payload.VIEWSTATEGENERATOR == "VG"
