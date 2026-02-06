import json
import os
from pathlib import Path
from typing import Any

from btsdatapy.core.constants import LOOKUPS_CONFIGS_PATH, TABLES_CONFIGS_PATH
from btsdatapy.core.models.config import BtsLookupConfig, BtsTableConfig


class Settings:
    cache_dir: Path = Path.home() / ".btsdatapy" / "cache"
    cache_enabled: bool = True


SETTINGS = Settings()


def _load_table_configs():
    tables = {}
    for data_library in os.listdir(TABLES_CONFIGS_PATH):
        library_path = TABLES_CONFIGS_PATH / data_library

        tables[data_library] = {}
        for database in os.listdir(library_path):
            database_path = library_path / database

            tables[data_library][database] = {}
            for table_file in os.listdir(database_path):
                table_name = table_file.rsplit(".", 1)[0]
                table_path = database_path / table_file

                with open(table_path, "r") as f:
                    json_data = json.load(f)

                    tables[data_library][database][table_name] = (
                        BtsTableConfig.model_validate(json_data)
                    )

    return tables


TABLE_CONFIGS = _load_table_configs()


def _load_lookups_from_dir(lookups_dir: Path) -> dict[str, Any]:
    lookups: dict[str, Any] = {}

    lookup_path = lookups_dir / "lookups.json"

    if not lookup_path.exists():
        return lookups

    with open(lookup_path, "r") as f:
        lookups_json = json.load(f)
        for lookup_json in lookups_json:
            lookup = BtsLookupConfig.model_validate(lookup_json)
            lookups[lookup.name] = lookup

    return lookups


def _load_lookup_configs(
    path: Path = LOOKUPS_CONFIGS_PATH,
) -> dict[str, Any]:
    lookups = {}

    dir_lookups = _load_lookups_from_dir(path)
    if dir_lookups:
        lookups["lookups"] = dir_lookups

    for sub_dir in os.listdir(path):
        sub_dir_path = path / sub_dir

        if not sub_dir_path.is_dir():
            continue

        lookups[sub_dir] = _load_lookup_configs(sub_dir_path)

    return lookups


LOOKUP_CONFIGS = _load_lookup_configs()
