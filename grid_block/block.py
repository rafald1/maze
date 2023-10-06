class Wall:
    def __init__(self):
        self.n = True
        self.e = True
        self.s = True
        self.w = True


class Block:
    def __init__(self, x_index, y_index):
        self.x_index = x_index
        self.y_index = y_index
        self.wall = Wall()
        self.visited = False
        self.revisited = False
        self.part_of_path = False

    def __eq__(self, other):
        return self.x_index == other.x_index and self.y_index == other.y_index

    # Used by heapq.heappush in PriorityQueue
    def __lt__(self, other):
        return self.x_index + self.y_index < other.x_index + other.y_index

    def __repr__(self):
        return f"Block({self.x_index}, {self.y_index})"

    @property
    def indices(self):
        return self.x_index, self.y_index

    def look_for_neighbour(self, grid):
        """Used when building a maze.
        Creates a list of neighbours that haven't been visited yet of the current block."""
        neighbours = []
        no_of_columns = grid[-1].x_index + 1
        no_of_rows = grid[-1].y_index + 1
        grid_index = no_of_columns * self.y_index + self.x_index
        # Check if it is possible for current block to have N, E, S and W neighbours
        # and if that neighbour hasn't been visited yet.
        if self.y_index != 0:
            north_neighbour_index = grid_index - no_of_columns
            if not grid[north_neighbour_index].visited:
                neighbours.append(grid[north_neighbour_index])
        if self.x_index != no_of_columns - 1:
            east_neighbour_index = grid_index + 1
            if not grid[east_neighbour_index].visited:
                neighbours.append(grid[east_neighbour_index])
        if self.y_index != no_of_rows - 1:
            south_neighbour_index = grid_index + no_of_columns
            if not grid[south_neighbour_index].visited:
                neighbours.append(grid[south_neighbour_index])
        if self.x_index != 0:
            west_neighbour_index = grid_index - 1
            if not grid[west_neighbour_index].visited:
                neighbours.append(grid[west_neighbour_index])
        return neighbours

    def remove_wall_between_two_blocks(self, other_block):
        """Used when building a maze.
        Removes proper walls of two adjacent blocks"""
        if self.x_index < other_block.x_index:
            self.wall.e = False
            other_block.wall.w = False
        elif self.x_index > other_block.x_index:
            self.wall.w = False
            other_block.wall.e = False
        elif self.y_index < other_block.y_index:
            self.wall.s = False
            other_block.wall.n = False
        elif self.y_index > other_block.y_index:
            self.wall.n = False
            other_block.wall.s = False

    def determine_valid_neighbours(self, grid):
        """Used when solving a maze.
        Creates a list of valid neighbours (no wall between) of the current block."""
        neighbours = []
        no_of_columns = grid[-1].x_index + 1
        grid_index = no_of_columns * self.y_index + self.x_index
        if not self.wall.n:
            north_neighbour_index = grid_index - no_of_columns
            neighbours.append(grid[north_neighbour_index])
        if not self.wall.e:
            east_neighbour_index = grid_index + 1
            neighbours.append(grid[east_neighbour_index])
        if not self.wall.s:
            south_neighbour_index = grid_index + no_of_columns
            neighbours.append(grid[south_neighbour_index])
        if not self.wall.w:
            west_neighbour_index = grid_index - 1
            neighbours.append(grid[west_neighbour_index])
        return neighbours

    def reset_visited_revisited(self):
        """Allows for the visited and revisited attribute to be used when solving a maze to visualize progress
        and the shortest path found."""
        self.visited = False
        self.revisited = False
