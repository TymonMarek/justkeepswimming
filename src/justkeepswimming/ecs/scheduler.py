import asyncio
import copy
import logging
from typing import Any, Dict, Set, Type

from justkeepswimming.datatypes.dag import (
    DirectedAcyclicGraph,
    DirectedAcyclicGraphNode,
)
from justkeepswimming.debug.scopes import ProfilerScope
from justkeepswimming.ecs import Component, Processor, SceneContext
from justkeepswimming.systems.clock import TickContext
from justkeepswimming.utilities.context import EngineContext

logger = logging.getLogger(__name__)


class SchedulerException(Exception):
    pass


class ProcessorNotFoundException(SchedulerException):
    pass


class SystemDuplicateEntryException(SchedulerException):
    pass


class SystemConflictException(SchedulerException):
    pass


class ProcessorScheduler:
    def __init__(
        self, scene_context: SceneContext, engine_context: EngineContext
    ) -> None:
        self.processors: Set[Processor] = set()
        self._nodes: Dict[Processor, DirectedAcyclicGraphNode[Processor]] = {}
        self._graph: DirectedAcyclicGraph[Processor] = DirectedAcyclicGraph()
        self._execution_order: list[Set[Processor]] = []
        self.engine_context = engine_context
        self.scene_context = scene_context
        self.profiler = engine_context.profiler

    def __deepcopy__(self, memo: dict[int, Any]
                     | None) -> "ProcessorScheduler":
        new_scheduler = ProcessorScheduler(
            self.scene_context, self.engine_context)
        new_scheduler.processors = copy.deepcopy(self.processors, memo)
        new_scheduler._nodes = copy.deepcopy(self._nodes, memo)
        new_scheduler._graph = copy.deepcopy(self._graph, memo)
        new_scheduler._execution_order = copy.deepcopy(
            self._execution_order, memo)
        return new_scheduler

    def _fmt_components(self, components: frozenset[Type[Component]]) -> str:
        return "{" + ", ".join(comp.__name__ for comp in components) + "}"

    async def process_tick(
        self,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ) -> None:
        for system_group in self._execution_order:
            await asyncio.gather(
                *(
                    self._run_with_profiler(
                        system, tick_context, scene_context, engine_context
                    )
                    for system in system_group
                )
            )

    async def _run_with_profiler(
        self,
        system: Processor,
        tick_context: TickContext,
        scene_context: SceneContext,
        engine_context: EngineContext,
    ):
        with engine_context.profiler.scope(
            ProfilerScope.PROCESSOR, system.__class__.__name__
        ):
            return await system.update(
                tick_context,
                scene_context,
                engine_context
            )

    def add_processor(self, processor: Processor) -> None:
        debug_mode = self.engine_context.launch_options.debug
        if processor.debug_only and not debug_mode:
            logger.debug(
                "Skipping addition of debug-only system ",
                {processor},
                " in non-debug mode."
                )
        if processor in self.processors:
            raise SystemDuplicateEntryException(
                f"System {processor} is already in the scheduler."
            )
        self.processors.add(processor)
        processor.initialize(self.scene_context, self.engine_context)
        logger.debug(f"Added system {processor} to the scheduler.")
        self._rebuild()

    def remove_processor(self, processor: Processor) -> None:
        if processor not in self.processors:
            raise ProcessorNotFoundException(
                f"System {processor} not found in the scheduler."
            )
        self.processors.remove(processor)
        processor.maid.cleanup()
        processor.teardown(self.scene_context, self.engine_context)
        self._rebuild()

    def execution_order(self) -> list[Set[Processor]]:
        return self._execution_order

    def _explicit_order(self, a: Processor, b: Processor) -> int | None:
        if type(b) in a.before or type(a) in b.after:
            return -1
        if type(b) in a.after or type(a) in b.before:
            return 1
        return None

    def _rebuild(self) -> None:
        logger.debug("Rebuilding processor scheduler DAG")

        self._graph = DirectedAcyclicGraph()
        self._nodes = {}

        for processor in self.processors:
            node = DirectedAcyclicGraphNode(processor)
            self._nodes[processor] = node
            self._graph.insert_node(node)
            logger.debug(
                f"Inserted node for processor {processor} "
                f"(reads={self._fmt_components(processor.reads)}, "
                f"writes={self._fmt_components(processor.writes)})"
            )

        processor = list(self.processors)

        for i in range(len(processor)):
            for j in range(len(processor)):
                if i == j:
                    continue

                a = processor[i]
                b = processor[j]

                node_a = self._nodes[a]
                node_b = self._nodes[b]

                order = self._explicit_order(a, b)
                if order is not None:
                    if order < 0:
                        logger.debug(f"Explicit override: {a} runs BEFORE {b}")
                        self._graph.set_dependency(node_b, node_a)
                    else:
                        logger.debug(f"Explicit override: {a} runs AFTER {b}")
                        self._graph.set_dependency(node_a, node_b)
                    continue

                components_a_writes_that_b_reads = a.writes & b.reads
                if components_a_writes_that_b_reads:
                    logger.debug(
                        f"Inferred: {a} runs BEFORE {b} "
                        f"because {b} reads {
                            self._fmt_components(
                                components_a_writes_that_b_reads)
                        }"
                    )
                    self._graph.set_dependency(node_b, node_a)

                components_a_reads_that_b_writes = a.reads & b.writes
                if components_a_reads_that_b_writes:
                    logger.debug(
                        f"Inferred: {b} runs BEFORE {a} "
                        f"because {a} reads {
                            self._fmt_components(
                                components_a_reads_that_b_writes)
                        }"
                    )
                    self._graph.set_dependency(node_a, node_b)

                components_both_write = a.writes & b.writes
                if components_both_write:
                    if type(a) in b.alongside or type(b) in a.alongside:
                        ...
                    else:
                        raise SystemConflictException(
                            "Unresolved write-write conflict between ",
                            {a},
                            " and ",
                            {b},
                            f"on {self._fmt_components(components_both_write)}"
                        )

        self._execution_order = self._graph.parallel_sort()

        logger.debug(
            "Final execution layers: "
            + " -> ".join(
                ", ".join(type(processor).__name__ for processor in layer)
                for layer in self._execution_order
            )
        )

    def _find_processor(self, processor_type: Type[Processor]) -> Processor:
        for processor in self.processors:
            if isinstance(processor, processor_type):
                return processor
        raise ProcessorNotFoundException(
            f"Processor of type {processor_type.__name__} not found."
        )
