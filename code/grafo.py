import math
import sys

# This is the Grafo class that reads the graph and coordinates files
class Grafo:
    def __init__(self, map_path):
        self.adj_list = []  # Stores the neighbours IDs and weights
        self.coords   = []  # Stores the coordinates of the nodes
        self.num_nodes = 0  # Couple of counters that are useful
        self.num_edges = 0

        # These are the extensions for the files 
        graph_file = map_path + ".gr"
        coords_file = map_path + ".co"

        # This first part will load the graph (.gr)
        try:
            f = open(graph_file, 'r')
            line_count = 0
            for line in f:
                line_count += 1
                if not line: continue

                if line.startswith('p'):
                    parts = line.split()
                    self.num_nodes = int(parts[2])
                    self.num_edges = int(parts[3])
                    
                    # Preallocating the memory for a list
                    self.adj_list = [[] for _ in range(self.num_nodes + 1)]
                    self.coords = [None] * (self.num_nodes + 1)
                    continue

                # Separate the line format: a <u> <v> <w>
                if line.startswith('a'):
                    if not self.adj_list:
                        print(f"ERROR: Edge found before header at line {line_count}")
                        sys.exit(1)

                    parts = line.split()
                    u = int(parts[1])
                    v = int(parts[2])
                    w = int(parts[3])

                    if u > self.num_nodes or v > self.num_nodes:
                        bad_id = u if u > self.num_nodes else v
                        print(f"WARNING: Line {line_count}: Node ID {bad_id} exceeds declared size {self.num_nodes}. Skipped.")
                        continue

                    # This adds each edge to the adjacency list
                    # and updates the counter
                    self.adj_list[u].append((v, w))
            f.close()
        # In case the file decides not to work
        except FileNotFoundError:
            print("ERROR: Graph file missing")
            exit(1)

        # This second part will load the coordinates (.co)
        try:
            f = open(coords_file, 'r')
            for line in f:
                line_count += 1
                # Separate the line format: v <id> <lon> <lat>
                if line and line.startswith('v'):
                    parts = line.split()
                    node_id = int(parts[1])

                    if node_id > self.num_nodes:
                        # We skip coordinates for nodes that fall outside our graph definition
                        continue

                    # We also need to adjust the coordinates
                    lon = int(parts[2]) / 1000000.0
                    lat = int(parts[3]) / 1000000.0
                    # We store them as a tuple
                    self.coords[node_id] = (lat, lon)
            f.close()
        except FileNotFoundError:
            print("ERROR: Coordinates file missing")
            exit(1)

    # These two functions will be useful for the A* algorithm and get us
    # the neighbors and coordinates of a given node (from the adjacency list
    # and the coords dictionary defined at the beggining)
    def get_neighbors(self, node):
        if 0 <= node < len(self.adj_list):
            return self.adj_list[node]
        return []

    def get_coordinates(self, node):
        if 0 <= node < len(self.coords):
            return self.coords[node]
        return None