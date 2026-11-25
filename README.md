# Shortest-Path Solver (A* & Dijkstra)

An implementation of the A* search algorithm (using an admissible spherical-projection Euclidean heuristic) and Dijkstra's algorithm evaluated on road networks from the 9th DIMACS Implementation Challenge.

## Repository Contents

* **`code/`**: Python source files implementing the graph loader (`grafo.py`), priority queue (`abierta.py`), visited set (`cerrada.py`), search engine (`algoritmo.py`), and CLI entry point (`main.py`).
* **`data.zip`**: Compressed archive containing the graph (`.gr`) and coordinate (`.co`) files for two sample networks: **New York City (`NY`)** and **Great Lakes (`LKS`)**.
* **`docs/`**: Contains the full methodology and benchmark analysis report (`Distances_Project.pdf`).

## Dataset Note

Due to GitHub file-size constraints, only the **New York City (`USA-road-d.NY`)** and **Great Lakes (`USA-road-d.LKS`)** road networks are bundled in this repository.

* **Official DIMACS Shortest Paths Dataset:** https://www.diag.uniroma1.it/challenge9/download.shtml

## Prerequisites

* Python 3.7 or higher (uses only the Python standard library; no external packages required).

## How to Run

1. **Clone the repository** and navigate into the project folder.

2. **Extract the map files** from `data.zip` into the project root (this creates the `data/` directory containing the `.gr` and `.co` files):
   * **macOS / Linux:**
     ```bash
     unzip data.zip
     ```
   * **Windows (PowerShell):**
     ```powershell
     Expand-Archive -Path data.zip -DestinationPath .
     ```

3. **Run the solver** from the project root directory using the following syntax:
   ```bash
   python code/main.py <start_node> <end_node> <map_prefix> <output_file> [-H | -B]
   ```

   **Arguments:**
   * `<start_node>`: Integer ID of the origin vertex (e.g., `1`).
   * `<end_node>`: Integer ID of the destination vertex (e.g., `1000`).
   * `<map_prefix>`: Path to the map files without the `.gr` or `.co` extension.
   * `<output_file>`: Path where the reconstructed shortest path will be saved.
   * `[-H | -B]` *(optional)*: Use `-H` for A* with the distance heuristic (defaulT) or `-B` for Dijkstra's algorithm.

### Example Commands

**Run A* (with heuristic) on the New York City network:**
```bash
python code/main.py 1 1000 data/USA-road-d.NY output.txt -H
```

**Run Dijkstra's algorithm (brute force) on the Great Lakes network:**
```bash
python code/main.py 1 5000 data/USA-road-d.LKS output.txt -B
```