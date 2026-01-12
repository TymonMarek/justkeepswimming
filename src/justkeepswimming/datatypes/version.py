class SemanticVersion:
    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def is_compatible_with(self, other: "SemanticVersion") -> bool:
        return self.major == other.major and self.minor >= other.minor
