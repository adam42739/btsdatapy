from pathlib import Path

import pandas as pd
from btsdatapy.core.config import SETTINGS
from btsdatapy.core.models.templates import (
    BtsDatabase,
    BtsDataLibrary,
    BtsLookup,
    BtsTable,
)


def set_cache_dir(cache_dir: str):
    SETTINGS.cache_dir = cache_dir


def set_cache_enabled(enabled: bool):
    SETTINGS.cache_enabled = enabled


def _get_path(
    data_library: BtsDataLibrary,
    database: BtsDatabase = None,
    table: BtsTable = None,
    lookup: BtsLookup = None,
) -> Path:
    if database and table and not lookup:
        path = SETTINGS.cache_dir / str(data_library) / str(database) / str(table)
    elif lookup and not (database or table):
        path = SETTINGS.cache_dir / str(data_library) / "lookup" / str(lookup)
    else:
        raise ValueError(
            "Invalid combination of parameters for cache path. "
            "Must specify either (data_library, database, table) "
            "or (data_library, lookup)."
        )

    return path.with_suffix(".parquet")


def is_cached(
    data_library: BtsDataLibrary,
    database: BtsDatabase = None,
    table: BtsTable = None,
    lookup: BtsLookup = None,
) -> bool:
    path = _get_path(data_library, database, table, lookup)
    return path.exists()


def get_cache(
    data_library: BtsDataLibrary,
    database: BtsDatabase = None,
    table: BtsTable = None,
    lookup: BtsLookup = None,
) -> pd.DataFrame:
    if not is_cached(data_library, database, table, lookup):
        raise FileNotFoundError("Requested cache file does not exist.")

    path = _get_path(data_library, database, table, lookup)

    return pd.read_parquet(path)


def set_cache(
    df: pd.DataFrame,
    data_library: BtsDataLibrary,
    database: BtsDatabase = None,
    table: BtsTable = None,
    lookup: BtsLookup = None,
):
    path = _get_path(data_library, database, table, lookup)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path)
