from data_types.priority_queue import PriorityQueue
from maze_solving.utils import reset_grid, build_shortest_path


class AStar:
    """Used to solve a maze using A* algorithm."""
    def __init__(self, grid, start_block, goal_block):
        self.current_block = None
        self.grid = grid
        self.start_block = start_block
        self.goal_block = goal_block
        self.p_queue = PriorityQueue()
        self.p_queue.put(self.start_block, 0)  # Put the starting block to the priority queue
        self.g_values = {self.start_block.indices: 0}
        # Predecessors are used to keep track of discovered neighbours and to build the shortest path.
        # It stores the key, value pairs of indices of discovered neighbour
        # and indices of block that discover such a neighbour
        self.predecessors = {start_block.indices: (-1, -1)}
        reset_grid(self.grid)

    @staticmethod
    def manhattan_distance(block, other_block):
        x1, y1 = block.indices
        x2, y2 = other_block.indices
        return abs(x1 - x2) + abs(y1 - y2)

    def iterate(self):
        """1. Get an element from the priority queue.
        2. Mark the current block as visited.
        3. Check if the current block is the goal block. Stop iterating if it is.
        4. Look for valid neighbours.
        5. For every neighbour found check if it has already been discovered (by checking predecessors)
            and if it hasn't been discovered yet:
            a) Calculate g value which indicates the steps needed to reach the starting block from that neighbour
                and store it.
            b) Calculate h value which indicates the distance between that neighbour and the goal block
                using Manhattan Distance.
            c) Calculate f value which indicates priority value.
            d) Put that neighbour with calculated f value to the priority queue.
            e) Add that neighbour to the predecessors dictionary to know it has been discovered
                and to store information about block that discovered it.
        6. Continue with next iteration."""

        self.current_block = self.p_queue.get()
        self.current_block.visited = True
        if self.current_block == self.goal_block:
            build_shortest_path(self.grid, self.predecessors, self.start_block, self.goal_block)
            return True

        neighbours = self.current_block.determine_valid_neighbours(self.grid)
        for neighbour in neighbours:
            if neighbour.indices not in self.predecessors:
                g_value = self.g_values[self.current_block.indices] + 1
                self.g_values[neighbour.indices] = g_value
                h_value = self.manhattan_distance(self.goal_block, neighbour)
                f_value = g_value + h_value
                self.p_queue.put(neighbour, f_value)
                self.predecessors[neighbour.indices] = self.current_block.indices
        return False
