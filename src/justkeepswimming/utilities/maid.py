from typing import Any

from justkeepswimming.utilities.signal import Connection


class Maid:
    def __init__(self) -> None:
        self._connections: list[Connection[Any]] = []

    def add(self, obj: Any) -> None:
        if isinstance(obj, Connection):
            self._connections.append(obj)

    def cleanup(self) -> None:
        for connection in self._connections:
            try:
                connection.disconnect()
            except Exception:
                if connection in connection.signal.connections:
                    connection.signal.disconnect(connection)
        self._connections.clear()
