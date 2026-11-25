import math
import time
from abierta import OpenList
from cerrada import ClosedList

class AStar:
    def __init__(self, graph):
        self.graph = graph
        self.exp_nodes = 0

        # These are physics constants we will use later
        self.rad_mult = math.pi / 180.0
        self.R = 63710000.0  # In decimeters

        # Cacheing information for better perfomance
        self.goal_lat_rad = None
        self.goal_lon_rad = None
        self.goal_cos = None

    # The Euclidean heuristic function
    def heuristic(self, u):
        # This is for the Dijkstra algorithm: no heuristic
        if self.goal_lat_rad is None:
            return 0.0

        # This is so it doesn't crash if coordinates are missing
        coords_u = self.graph.get_coordinates(u)
        if not coords_u:
            return 0.0

        # Converting into radians
        lat_u_rad = coords_u[0] * self.rad_mult
        lon_u_rad = coords_u[1] * self.rad_mult

        # Calculate differences, accounting for Earth's curvature
        d_lat = lat_u_rad - self.goal_lat_rad
        d_lon = (lon_u_rad - self.goal_lon_rad) * self.goal_cos

        # Euclidean distance on the projected plane
        rad_dist = math.hypot(d_lat, d_lon)
        
        # Scale to actual distance
        return self.R * rad_dist

    # The A* algorithm implementation
    def solve(self, start, goal, method=None):
        
        # Make sure the start and goal nodes are valid
        if goal > self.graph.num_nodes or start > self.graph.num_nodes:
            print("ERROR: Start or Goal not in graph")
            return False, {}, 0, 0.0

        # This information we have to keep track of for performance analysis
        start_time = time.perf_counter()
        self.exp_nodes = 0

        # If we use "-B" we use brute force. if we use "-H" we use heuristic
        # If flag not selected, default to heuristic
        use_heuristic = True
        if method == "-B":
            use_heuristic = False

        open_list = OpenList()
        closed_list = ClosedList()

        # This will help us reconstruct the path later
        parents = {}   
        g_costs = {}   

        # This is precomputing information that we will use in each run so that
        # we don't waste time recalculating it each time in the heuristic function
        if use_heuristic:
            coords_goal = self.graph.get_coordinates(goal)
            coords_start = self.graph.get_coordinates(start)

            if coords_goal and coords_start:
                self.goal_lat_rad = coords_goal[0] * self.rad_mult
                self.goal_lon_rad = coords_goal[1] * self.rad_mult
            
                # To make sure this heuristic is admissible on a sphere we have to scale
                # longitude by the cosine of the latitude closest to a Pole so that we
                # never overestimate the width of a degree of longitude
                start_lat_rad = coords_start[0] * self.rad_mult
                self.goal_cos = min(math.cos(start_lat_rad), math.cos(self.goal_lat_rad))
            else:
                # In case coordinates are missing
                self.goal_lat_rad = None
                self.goal_lon_rad = None
                self.goal_cos = 1.0
        else:
            # For when doing brute force
            self.goal_lat_rad = None

        # Here we start the actual algorithm
        g_costs[start] = 0
        parents[start] = None

        # For the first case
        h_start = self.heuristic(start)
        open_list.put(start, g_costs[start] + h_start)

        found = False
        final_cost = 0

        # This is the main loop of the A* algorithm
        while not open_list.is_empty():
            current = open_list.get()
            self.exp_nodes += 1

            # For when we finally find the solution
            if current == goal:
                found = True
                final_cost = g_costs[current]
                break

            # If we have already visited the node, skip it
            if closed_list.contains(current):
                continue

            # Mark the current node as visited
            curr_g = g_costs[current]
            closed_list.put(current, curr_g)

            # Explore each neighbor of the current node
            for neighbor, weight in self.graph.get_neighbors(current):
                tentative_g = curr_g + weight

                if closed_list.contains(neighbor):
                    continue

                # We turn the cost into infinity to nuke it out of existence
                old_g = g_costs.get(neighbor, float('inf'))
                if tentative_g < old_g:
                    parents[neighbor] = (current, weight)
                    g_costs[neighbor] = tentative_g

                    # Calculate f_cost, with heuristic returning 0
                    # if we are doing Dijkstra
                    h_cost = self.heuristic(neighbor)
                    f_cost = tentative_g + h_cost
                    
                    open_list.put(neighbor, f_cost)

        end_time = time.perf_counter()
        return found, parents, final_cost, end_time - start_time
