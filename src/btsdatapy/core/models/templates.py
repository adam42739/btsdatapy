from enum import Enum


class BtsDataLibrary(Enum):
    AVAIATION = "aviation"

    def __str__(self) -> str:
        return self.value


class BtsDatabase(Enum):
    def __str__(self) -> str:
        return self.value


class BtsTable(Enum):
    def __str__(self) -> str:
        return self.value


class BtsLookup(Enum):
    def __str__(self) -> str:
        return self.value
