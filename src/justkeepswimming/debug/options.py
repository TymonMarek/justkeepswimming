from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProfileOptions:
    dump_path: Path
    enabled: bool = True
    history_length: int = 1000
