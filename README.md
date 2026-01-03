# justkeepswimming

A small game about a fish in the deep sea.

## Features

- Entity Component System (ECS) architecture
- DAG-based system scheduler for deterministic execution order
- Scene management with lazy/eager loading strategies
- **Debug DAG Visualizer**: Visual representation of system execution graph (see [docs/DAG_VISUALIZER.md](docs/DAG_VISUALIZER.md))

## Usage

Run the game:
```bash
python -m justkeepswimming
```

Enable DAG visualization for debugging:
```bash
python -m justkeepswimming --debug-dag
```

For more verbose logging:
```bash
python -m justkeepswimming --debug-dag -v 3
```
