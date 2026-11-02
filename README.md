# Dungeon Treasure Hunt

A 2D desktop demonstration of **Uniform Cost Search (UCS)**, **Greedy Best-First Search**, and **A\*** on the same weighted grid.

## Requirements

- Python 3.10 or newer
- Pygame (only external dependency)

## Getting started (Windows / VS Code)

Open this folder in VS Code, open its terminal, and run:

```powershell
py -m pip install -r requirements.txt
py main.py
```

If your terminal recognizes `python` but not `py`, replace `py` with `python`.

## Controls

- Choose **UCS**, **Greedy**, or **A***.
- Choose **Basic**, **Walls**, or **Weighted** scenario.
- Click **START SEARCH** (or press `Space`); searched cells animate blue, final path yellow.
- Click **RESET** (or press `R`) to clear.
- Use `+` / `-` to adjust animation speed (1x to 8x).
- The statistics panel shows **total path cost**, **path length (moves)**, **unique explored nodes**, and **search-only execution time**.

## Terrain and algorithm rules

| Tile | Meaning | Cost of entering |
|---|---|---|
| `S` | Start | no charge until a tile is entered |
| `T` | Treasure | 1 |
| `.` | Normal floor | 1 |
| `M` | Mud | 3 |
| `L` | Lava | 5 |
| `#` | Wall | impassable |

Moves are only up/down/left/right. All search algorithms use the same neighbor order and terrain costs. The heuristic is **Manhattan distance**, admissible because every traversable tile costs at least 1. UCS and A* therefore find optimal-cost paths. Greedy uses heuristic only; its path may be more expensive. Ties in the priority queue are resolved in insertion order. The start counts as one explored node, if expanded. A* may expand a node again if its best `g` improves, but the explored metric counts unique nodes.

**Execution times** may fluctuate and be too small to compare reliably on tiny grids. Run many repetitions and report average/median if latency is part of the report. Animation time is not included.

## Run experiments and tests

```powershell
py -m experiments.run_experiments
py -m unittest discover -s tests -v
```

The experiment command writes `experiments/results.csv`. This is a baseline, not a benchmark averaged over many trials.

## Structure

- `main.py`: Pygame main loop, UI actions
- `config.py`: sizes, colors, tile costs
- `algorithms/`: UCS, Greedy and A* with shared priority-queue engine
- `game/`: grid, rendering, character/terrain definitions
- `visualization/`: animation and statistics
- `experiments/`: reproducible scenarios and CSV export
- `tests/`: basic path/cost and optimality checks

No outside graphics or fonts are needed; the game uses built-in drawing primitives and system fonts.
