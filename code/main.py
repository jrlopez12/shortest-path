#!/usr/bin/env python3

import sys
import re
from grafo import Grafo
from algoritmo import AStar

def main():
    # Make sure the correct amount of arguments are passed
    if (5 > len(sys.argv)) or (len(sys.argv) < 6) :
        print("Amount of arguments introduced incorrect")
        return

    # We need to  check that the node inputs are read as integers
    try:
        start_node = int(sys.argv[1])
        end_node = int(sys.argv[2])
    except ValueError:
        print("ERROR: Starting and ending points must be integers")
        return

    # We will also name the other two arguments, for clarity
    map_path = sys.argv[3]
    output_file = sys.argv[4]

    # This will be used if the method argument is given
    if len(sys.argv) == 6:
        method = sys.argv[5]

    # We call the Grafo class to read the map files 
    try:
        graph = Grafo(map_path)
    except OSError:
        print("ERROR: Unable to read files in map:", map_path)
        return
    
    # This is the first information that we have to print and that we get
    # from the Grafo class
    print(f"# vertices: {graph.num_nodes}")
    print(f"# edges: {graph.num_edges}")

    # We initilialize the A* solver from the algoritmo file, and save outputs
    solver = AStar(graph)
    if len(sys.argv) == 5:
        found, prev, cost, duration = solver.solve(start_node, end_node, method = "-H")
    else: 
        found, prev, cost, duration = solver.solve(start_node, end_node, method)

    if found:
        # Assuming we have found a path, we reconstruct the full path as a
        # list of node IDs. To do this we need to read backwards (given that
        # in the algoritmo we store each node's parent) and insert in the
        # first position of the list, until there are no more parents.
        path_nodes = [] 
        current = end_node 
        while current is not None: 
            path_nodes.insert(0, current) 
            prev_info = prev.get(current) 
            if prev_info is None: 
                break 
            parent = prev_info[0] 
            current = parent 

        # For ease of printing we will turn the output into a single string
        # We store the first node explictly, then for each next node we add the
        # - (cost) - nextnode structure that is stated
        output_line = str(path_nodes[0]) 
        for i in range(len(path_nodes) - 1): 
            next_node = path_nodes[i + 1] 
            parent, edge_cost = prev[next_node] 
            output_line += " - (" + str(edge_cost) + ") - " + str(next_node)

        # More information that we need to print out: cost, time and rate
        print(f"Optimal solution found with cost {cost}")
        print(f"Execution time: {duration:.2f} seconds")
        rate = solver.exp_nodes / duration
        print(f"# expansions: {solver.exp_nodes} ({rate:.2f} nodes/sec)")

        # Finally, we write the output line to the output file
        try:
            f = open(output_file, 'w')
            f.write(output_line + "\n")
            f.close()
        except OSError:
            print("ERROR: Could not write in output file")
            return
    # If no path was found, we print that and write to the output file
    else:
        print("\nNo path found between  nodes.")
        with open(output_file, 'w') as f:
            f.write("No solution found")

if __name__ == "__main__":
    main()