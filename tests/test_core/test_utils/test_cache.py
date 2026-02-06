from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from btsdatapy.core.utils import cache

TEST_DF_DICT = {"col1": ["val1"], "col2": ["val2"]}
TEST_DF = pd.DataFrame(TEST_DF_DICT)

TEST_TABLE = "test_table"
TEST_LOOKUP = "test_lookup"
TEST_USER_PARAMETERS = {"test_key": "test_value", "another_key": "another_value"}


def test_cache_toggle():
    cache.set_cache_enabled(False)
    assert cache.SETTINGS.cache_enabled is False

    cache.set_cache_enabled(True)
    assert cache.SETTINGS.cache_enabled is True


def test_cache_roundtrip_success():
    with TemporaryDirectory() as temp_dir:
        cache.set_cache_dir(temp_dir)

        cache.write_cache(TEST_DF, TEST_USER_PARAMETERS, table_id=TEST_TABLE)

        assert cache.is_cached(TEST_USER_PARAMETERS, table_id=TEST_TABLE) is True

        loaded = cache.read_cache(TEST_USER_PARAMETERS, table_id=TEST_TABLE)
        assert loaded.to_dict("list") == TEST_DF_DICT


def test_cache_roundtrip_failure():
    with TemporaryDirectory() as temp_dir:
        cache.set_cache_dir(temp_dir)

        cache.write_cache(TEST_DF, TEST_USER_PARAMETERS, lookup_id=TEST_LOOKUP)

        with pytest.raises(FileNotFoundError):
            cache.read_cache(TEST_USER_PARAMETERS, table_id=TEST_TABLE)


def test_cache_invalid_params():
    with TemporaryDirectory() as temp_dir:
        cache.set_cache_dir(temp_dir)

        with pytest.raises(ValueError):
            cache.write_cache(
                TEST_DF,
                TEST_USER_PARAMETERS,
                table_id=TEST_TABLE,
                lookup_id=TEST_LOOKUP,
            )
