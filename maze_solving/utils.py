def reset_grid(grid):
    """Resets the grid to allow solving process visualization."""
    for block in grid:
        block.reset_visited_revisited()


def build_shortest_path(grid, predecessors, start_block, goal_block):
    """Used to build the shortest path found by an algorithm.
    Uses revisited attribute of a block to show the shortest path."""
    goal_block.revisited = True
    no_of_columns = grid[-1].x_index + 1
    current_block_indices = (goal_block.x_index, goal_block.y_index)

    while current_block_indices != (start_block.x_index, start_block.y_index):
        current_block_indices = predecessors[current_block_indices]
        grid_index = current_block_indices[1] * no_of_columns + current_block_indices[0]
        grid[grid_index].revisited = True
    start_block.revisited = True
