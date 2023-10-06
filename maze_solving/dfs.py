from data_types.stack import Stack
from maze_solving.utils import reset_grid, build_shortest_path


class DepthFirstSearch:
    """Used to solve a maze using Depth First Search algorithm."""
    def __init__(self, grid, start_block, goal_block):
        self.current_block = None
        self.grid = grid
        self.start_block = start_block
        self.goal_block = goal_block
        self.stack = Stack()
        self.stack.push(self.start_block)  # Push the starting block to the stack
        # Predecessors are used to keep track of discovered neighbours and to build the shortest path.
        # It stores the key, value pairs of indices of discovered neighbour
        # and indices of block that discover such a neighbour
        self.predecessors = {start_block.indices: (-1, -1)}
        reset_grid(self.grid)

    def iterate(self):
        """1. Remove an element from the stack.
        2. Mark the current block as visited.
        3. Check if the current block is the goal block. Stop iterating if it is.
        4. Look for valid neighbours.
        5. For every neighbour found check if it has already been discovered (by checking predecessors)
            and if it hasn't been discovered yet:
            a) Push that neighbour to the stack.
            b) Add that neighbour to the predecessors dictionary to know it has been discovered
                and to store information about block that discovered it.
        6. Continue with next iteration."""
        self.current_block = self.stack.pop()
        self.current_block.visited = True
        if self.current_block == self.goal_block:
            build_shortest_path(self.grid, self.predecessors, self.start_block, self.goal_block)
            return True

        neighbours = self.current_block.determine_valid_neighbours(self.grid)
        for neighbour in neighbours:
            if neighbour.indices not in self.predecessors:
                self.stack.push(neighbour)
                self.predecessors[neighbour.indices] = self.current_block.indices
        return False
