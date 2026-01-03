# DAG Visualizer - Debugging Tool

## Overview

The DAG Visualizer is a debugging feature that displays a visual representation of the system execution graph (Directed Acyclic Graph) in a separate window while the game is running. This tool helps developers understand and debug the order in which systems execute.

## Features

- **Separate Thread Execution**: Runs on a separate daemon thread to avoid blocking the main game thread
- **Thread-Safe Communication**: Uses `queue.Queue` for safe data passing between threads
- **Interactive Visualization**: Click on nodes to view detailed information about systems
- **Real-Time Updates**: Automatically updates when the system scheduler is rebuilt
- **Visual Representation**: Shows:
  - System nodes arranged in execution layers
  - Dependencies between systems (arrows)
  - Component read/write relationships
  - Execution order (layered layout)

## Usage

### Command Line

Enable the DAG visualizer using the `--debug-dag` flag:

```bash
python -m justkeepswimming --debug-dag
```

You can also combine it with verbosity settings:

```bash
python -m justkeepswimming --debug-dag -v 3
```

### Programmatic Usage

```python
from justkeepswimming.modules.game import Game

# Create game with visualizer enabled
game = Game(enable_dag_visualizer=True)
```

## Visualization Window

### Layout

The visualization window displays:
- **Title**: "System Execution DAG" at the top
- **Graph Area**: Main area showing nodes and edges
- **Node Details Panel**: Bottom area showing details of selected node
- **Instructions**: Bottom-right corner with usage instructions

### Node Representation

- **Node**: Circle with system name
- **Blue Color**: Normal node
- **Light Blue**: Selected node
- **Arrows**: Dependencies between systems (from dependency → to dependent)

### Interaction

1. **Click on a Node**: Displays detailed information about the system:
   - System name
   - Components it reads (green label)
   - Components it writes (red label)

2. **Close Window**: Closes the visualization window (game continues)

## Architecture

### Components

1. **DAGVisualizer Class** (`utilities/dag_visualizer.py`)
   - Main visualization controller
   - Manages the separate visualization thread
   - Handles thread-safe data updates

2. **GraphData, NodeData, EdgeData** (data classes)
   - Data structures for passing graph information between threads

3. **extract_graph_data_from_scheduler()** (function)
   - Extracts graph structure from SystemScheduler
   - Converts internal graph to visualization-friendly format

### Integration Points

The visualizer is integrated at several points:

1. **Game.__init__()**: Creates visualizer if enabled
2. **Game.start()**: Starts the visualization thread
3. **Game._quit()**: Stops the visualization thread
4. **Stage.__init__()**: Receives visualizer reference
5. **SceneHandle.get_scene()**: Passes visualizer to scenes
6. **Scene._process_systems()**: Updates visualizer with current graph data

### Thread Safety

- **Main Thread**: Game logic, system execution
- **Visualizer Thread**: Pygame window for visualization
- **Communication**: `queue.Queue` for thread-safe data passing
- **Updates**: Non-blocking updates from main thread to visualizer

## Implementation Details

### Data Flow

1. Systems added to scheduler → DAG built
2. Each frame: `Scene._process_systems()` extracts graph data
3. Graph data pushed to `queue.Queue`
4. Visualizer thread reads from queue (non-blocking)
5. Visualizer renders updated graph

### Performance

- **Minimal Overhead**: Graph extraction only happens once per frame
- **Non-Blocking**: Queue operations don't block game thread
- **Daemon Thread**: Automatically cleaned up when game exits
- **30 FPS Cap**: Visualization renders at 30 FPS to reduce CPU usage

### Colors

- **Background**: Dark blue-grey (30, 30, 40)
- **Nodes**: Steel blue (70, 130, 180)
- **Selected Node**: Light steel blue (100, 160, 210)
- **Edges**: Grey (150, 150, 150)
- **Text**: White (255, 255, 255)
- **Read Label**: Green (100, 200, 100)
- **Write Label**: Red (200, 100, 100)

## Example Output

For a simple game with three systems:

```
SceneSizeConstraintSystem  →  AspectRatioConstraintSystem  →  CameraSystem
     (Layer 0)                       (Layer 1)                   (Layer 2)
```

The visualization shows:
- SceneSizeConstraintSystem writes Transform
- AspectRatioConstraintSystem reads and writes Transform
- CameraSystem reads Transform and Camera

Dependencies are automatically resolved based on read/write relationships.

## Troubleshooting

### Window doesn't appear
- Check that pygame-ce is installed
- Ensure display is available (may not work in headless environments)
- Check logs for "DAG visualizer enabled" message

### No graph data shown
- Ensure systems are added to the scheduler
- Check that scenes are properly loaded
- Verify scheduler is being rebuilt

### Graph not updating
- Check for exceptions in Scene._process_systems()
- Verify visualizer thread is running
- Check queue is not full

## Future Enhancements

Possible improvements:
- Export graph to image file
- Zoom and pan controls
- Filter by component type
- Highlight critical paths
- Show execution timing statistics
- Animation of system execution flow
