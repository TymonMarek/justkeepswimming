from argparse import Action, ArgumentParser, Namespace
from typing import Sequence


class VerbosityAction(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Sequence[str] | None,
        option_string: str | None = None,
    ) -> None:
        count = option_string.count("v") if option_string else 0
        level = max(1, min(3, count))
        setattr(namespace, self.dest, level)
