from unittest.mock import patch

import pandas as pd
from btsdatapy.core.config import TABLE_CONFIGS
from btsdatapy.core.services.fetch import fetch_table

TEST_COLUMNS = ["FlightDate", "TailNumber", "ActualDepartureTime"]
TEST_COLUMNS_EXTRA = [
    "FlightDate",
    "TailNumber",
    "ActualDepartureTime",
    "Origin",
    "Destination",
]


TEST_TABLE_CONFIG = TABLE_CONFIGS["aviation"]["airline_otp"]["reporting_carrier_otp"]
TEST_USER_PARAMETERS = [{"year": "2022", "month": "1"}, {"year": "2023", "month": "4"}]

TEST_TABLE = pd.DataFrame(
    {
        "FlightDate": ["2022-01-15", "2023-04-20"],
        "TailNumber": ["N12345", "N67890"],
        "ActualDepartureTime": ["08:00", "14:30"],
    }
)
TEST_TABLE_EXTRA = pd.DataFrame(
    {
        "Origin": ["JFK", "LAX"],
        "Destination": ["LAX", "JFK"],
        "FlightDate": ["2022-01-15", "2023-04-20"],
        "TailNumber": ["N12345", "N67890"],
        "ActualDepartureTime": ["08:00", "14:30"],
    }
)


def test_fetch_table_no_cache():
    with (
        patch("btsdatapy.core.services.fetch.SETTINGS.cache_enabled", True),
        patch("btsdatapy.core.services.fetch.is_cached", return_value=False),
        patch("btsdatapy.core.services.fetch.BtsStatefulClient") as mock_client_class,
        patch("btsdatapy.core.services.fetch.write_cache") as mock_write_cache,
    ):
        mock_fetch = mock_client_class.return_value.fetch_table
        mock_fetch.return_value = TEST_TABLE

        result = fetch_table(
            TEST_TABLE_CONFIG,
            columns=TEST_COLUMNS,
            all_user_parameters=TEST_USER_PARAMETERS,
        )

        assert mock_fetch.call_count == len(TEST_USER_PARAMETERS)
        assert mock_write_cache.call_count == len(TEST_USER_PARAMETERS)
        assert list(result.columns) == TEST_COLUMNS
        assert result.shape[0] == TEST_TABLE.shape[0] * len(TEST_USER_PARAMETERS)


def test_fetch_table_with_cache():
    with (
        patch("btsdatapy.core.services.fetch.SETTINGS.cache_enabled", True),
        patch("btsdatapy.core.services.fetch.is_cached", return_value=True),
        patch("btsdatapy.core.services.fetch.read_cache", return_value=TEST_TABLE),
        patch("btsdatapy.core.services.fetch.BtsStatefulClient") as mock_client_class,
        patch("btsdatapy.core.services.fetch.write_cache") as mock_write_cache,
    ):
        mock_fetch = mock_client_class.return_value.fetch_table
        mock_fetch.return_value = TEST_TABLE_EXTRA

        result = fetch_table(
            TEST_TABLE_CONFIG,
            columns=TEST_COLUMNS_EXTRA,
            all_user_parameters=TEST_USER_PARAMETERS,
        )

        assert mock_fetch.call_count == 2
        assert mock_write_cache.call_count == 2
        assert list(result.columns) == TEST_COLUMNS_EXTRA
        assert result.shape[0] == TEST_TABLE.shape[0] * len(TEST_USER_PARAMETERS)


def test_fetch_table_cache_disabled():
    with (
        patch("btsdatapy.core.services.fetch.SETTINGS.cache_enabled", False),
        patch("btsdatapy.core.services.fetch.is_cached", return_value=True),
        patch("btsdatapy.core.services.fetch.read_cache", return_value=TEST_TABLE),
        patch("btsdatapy.core.services.fetch.BtsStatefulClient") as mock_client_class,
        patch("btsdatapy.core.services.fetch.write_cache") as mock_write_cache,
    ):
        mock_fetch = mock_client_class.return_value.fetch_table
        mock_fetch.return_value = TEST_TABLE

        result = fetch_table(
            TEST_TABLE_CONFIG,
            columns=TEST_COLUMNS,
            all_user_parameters=TEST_USER_PARAMETERS,
        )

        assert mock_fetch.call_count == len(TEST_USER_PARAMETERS)
        assert mock_write_cache.call_count == len(TEST_USER_PARAMETERS)
        assert list(result.columns) == TEST_COLUMNS
        assert result.shape[0] == TEST_TABLE.shape[0] * len(TEST_USER_PARAMETERS)
