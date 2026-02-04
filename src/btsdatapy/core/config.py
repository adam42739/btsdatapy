from pathlib import Path


class Settings:
    cache_dir: Path = Path.home() / ".btsdatapy" / "cache"
    cache_enabled: bool = True


SETTINGS = Settings()
