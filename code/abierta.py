import heapq

class OpenList:
    def __init__(self):
        # The heap will store tuples of (priority, node)
        self.heap = [] 
    
    # These three functions will allow us to manage the open list
    def is_empty(self):
        return len(self.heap) == 0
    
    def put(self, node, priority):
        # Store as tuple (priority, node) so heapq sorts by priority first
        heapq.heappush(self.heap, (priority, node))
    
    def get(self):
        # Returns the node with the lowest cost
        return heapq.heappop(self.heap)[1]