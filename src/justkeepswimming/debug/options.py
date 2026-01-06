from dataclasses import dataclass


@dataclass
class ProfileOptions:
    enabled: bool = True
    history_length: int = 1000
