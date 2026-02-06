from pathlib import Path

import pandas as pd
from btsdatapy.core.config import SETTINGS


def set_cache_dir(cache_dir: str | Path):
    SETTINGS.cache_dir = Path(cache_dir)


def set_cache_enabled(enabled: bool):
    SETTINGS.cache_enabled = enabled


def _get_path(
    path_id: str,
    table_id: str | None = None,
    lookup_id: str | None = None,
) -> Path:
    if table_id and not lookup_id:
        path = SETTINGS.cache_dir / "tables" / table_id / path_id
    elif lookup_id and not table_id:
        path = SETTINGS.cache_dir / "lookups" / lookup_id / path_id
    else:
        raise ValueError(
            "Invalid combination of parameters for cache path. "
            "Must specify either `table_id` or `lookup_id`."
        )

    return path.with_suffix(".parquet")


def is_cached(
    path_id: str,
    table_id: str | None = None,
    lookup_id: str | None = None,
) -> bool:
    path = _get_path(path_id, table_id, lookup_id)
    return path.exists()


def read_cache(
    path_id: str,
    table_id: str | None = None,
    lookup_id: str | None = None,
) -> pd.DataFrame:
    if not is_cached(path_id, table_id, lookup_id):
        raise FileNotFoundError("Requested cache file does not exist.")

    path = _get_path(path_id, table_id, lookup_id)

    return pd.read_parquet(path)


def write_cache(
    df: pd.DataFrame,
    path_id: str,
    table_id: str | None = None,
    lookup_id: str | None = None,
):
    path = _get_path(path_id, table_id, lookup_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path)
