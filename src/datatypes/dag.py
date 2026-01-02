from __future__ import annotations

from collections import deque
from typing import Generic, TypeVar, Set, Dict, List

T = TypeVar("T")


class DirectedAcyclicGraphError(Exception):
    pass


class NodeNotFoundError(DirectedAcyclicGraphError):
    pass


class NodeAlreadyExistsError(DirectedAcyclicGraphError):
    pass


class CyclicalDependencyError(DirectedAcyclicGraphError):
    pass


class DirectedAcyclicGraphNode(Generic[T]):
    __slots__ = ("value", "depends_on")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.depends_on: Set[DirectedAcyclicGraphNode[T]] = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"


class DirectedAcyclicGraph(Generic[T]):
    def __init__(self) -> None:
        self._nodes: Set[DirectedAcyclicGraphNode[T]] = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nodes={len(self._nodes)})"

    def insert_node(
        self, node: DirectedAcyclicGraphNode[T]
    ) -> DirectedAcyclicGraphNode[T]:
        if node in self._nodes:
            raise NodeAlreadyExistsError(f"{node} already exists in the graph.")
        self._nodes.add(node)
        return node

    def _require_node(self, node: DirectedAcyclicGraphNode[T]) -> None:
        if node not in self._nodes:
            raise NodeNotFoundError(f"{node} is not part of this graph.")

    def set_dependency(
        self, node: DirectedAcyclicGraphNode[T], dependency: DirectedAcyclicGraphNode[T]
    ) -> None:
        self._require_node(node)
        self._require_node(dependency)

        if node is dependency:
            raise CyclicalDependencyError(f"{node} cannot depend on itself.")

        visited: Set[DirectedAcyclicGraphNode[T]] = set()
        pending: Set[DirectedAcyclicGraphNode[T]] = {dependency}

        while pending:
            current = pending.pop()

            if current is node:
                raise CyclicalDependencyError(
                    f"Cannot add dependency: {node} depends on {dependency}, "
                    f"but {dependency} already depends on {node}."
                )

            if current in visited:
                continue

            visited.add(current)
            pending.update(current.depends_on)

        node.depends_on.add(dependency)

    def topological_sort(self) -> List[T]:
        in_degree: Dict[DirectedAcyclicGraphNode[T], int] = {
            node: 0 for node in self._nodes
        }

        for node in self._nodes:
            for _ in node.depends_on:
                in_degree[node] += 1

        queue: deque[DirectedAcyclicGraphNode[T]] = deque(
            node for node, degree in in_degree.items() if degree == 0
        )

        result: List[T] = []

        while queue:
            current = queue.popleft()
            result.append(current.value)

            for dependent in self._nodes:
                if current in dependent.depends_on:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        if len(result) != len(self._nodes):
            raise CyclicalDependencyError("Graph contains a cycle.")

        return result

    def parallel_sort(self) -> List[Set[T]]:
        in_degree: Dict[DirectedAcyclicGraphNode[T], int] = {
            node: 0 for node in self._nodes
        }

        for node in self._nodes:
            for _ in node.depends_on:
                in_degree[node] += 1

        zero_in_degree: Set[DirectedAcyclicGraphNode[T]] = {
            node for node, degree in in_degree.items() if degree == 0
        }

        layers: List[Set[T]] = []

        while zero_in_degree:
            current_layer: Set[T] = set()
            next_zero_in_degree: Set[DirectedAcyclicGraphNode[T]] = set()

            for node in zero_in_degree:
                current_layer.add(node.value)

                for dependent in self._nodes:
                    if node in dependent.depends_on:
                        in_degree[dependent] -= 1
                        if in_degree[dependent] == 0:
                            next_zero_in_degree.add(dependent)

            layers.append(current_layer)
            zero_in_degree = next_zero_in_degree

        total = sum(len(layer) for layer in layers)
        if total != len(self._nodes):
            raise CyclicalDependencyError("Graph contains a cycle.")

        return layers
