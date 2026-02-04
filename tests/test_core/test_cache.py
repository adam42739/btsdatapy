from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from btsdatapy.core import cache

TEST_DF_DICT = {"col1": ["val1"], "col2": ["val2"]}
TEST_DF = pd.DataFrame(TEST_DF_DICT)


class _Nameable:
    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return self._name


TEST_LIB = _Nameable("libA")
TEST_DB = _Nameable("dbA")
TEST_TABLE = _Nameable("tableA")
TEST_LOOKUP = _Nameable("lookupA")

_CREATED = set()


def _mock_to_parquet(self, path, *args, **kwargs):
    _CREATED.add(str(path))


def _mock_read_parquet(path, *args, **kwargs):
    return TEST_DF


def _mock_exists(self):
    return str(self) in _CREATED


def test_table_cache_roundtrip_success():
    global _CREATED
    _CREATED = set()

    with (
        patch("pandas.DataFrame.to_parquet", new=_mock_to_parquet),
        patch("pandas.read_parquet", new=_mock_read_parquet),
        patch.object(Path, "exists", new=_mock_exists),
    ):
        cache.set_cache(TEST_DF, TEST_LIB, database=TEST_DB, table=TEST_TABLE)

        assert cache.is_cached(TEST_LIB, database=TEST_DB, table=TEST_TABLE) is True

        loaded = cache.get_cache(TEST_LIB, database=TEST_DB, table=TEST_TABLE)
        assert loaded.to_dict("list") == TEST_DF_DICT


def test_lookup_cache_roundtrip_failure():
    global _CREATED
    _CREATED = set()

    with (
        patch("pandas.DataFrame.to_parquet", new=_mock_to_parquet),
        patch("pandas.read_parquet", new=_mock_read_parquet),
        patch.object(Path, "exists", new=_mock_exists),
    ):
        cache.set_cache(TEST_DF, TEST_LIB, lookup=TEST_LOOKUP)

        with pytest.raises(FileNotFoundError):
            cache.get_cache(TEST_LIB, database=TEST_DB, table=TEST_TABLE)
