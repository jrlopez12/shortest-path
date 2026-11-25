class ClosedList:
    def __init__(self):
        # Dictionary maps each node to it's cost so far
        self.visited = {}

    # These three functions will allow us to manage the closed list
    def put(self, node, cost):
        self.visited[node] = cost

    def get(self, node):
        return self.visited[node]

    def contains(self, node):
        return node in self.visited