from random import choice

from data_types.stack import Stack


class RandomizedDepthFirstSearch:
    """Used to build a maze using DepthFirstSearch that randomly chooses one not visited neighbour."""
    def __init__(self, grid):
        self.grid = grid
        self.stack = Stack()
        self.is_path_found = False
        self.current_block = self.grid[0]
        self.current_block.visited = True

    def mark_blocks_as_part_of_path(self, last_block):
        """Mark proper blocks in a grid_block to be able to display the shortest path
        based on a stack used during building a maze and the last block that has been just reached."""
        last_block.part_of_path = True

        for i in range(self.stack.size()):
            block = self.stack.peak(i)
            block.part_of_path = True

    def iterate(self):
        """1. Look for not visited neighbours of the current block.
        2. Randomly choose a neighbour from the available ones if possible.
        3. If you found a neighbour:
            a) Add current block to the stack.
            b) Additional step: Check if the neighbour is the last block of the grid
                and path hasn't been discovered to be able to store the path.
            c) Remove walls between the current block and the selected neighbour.
            d) Make the neighbour the current block and mark it as visited.
        4. If the current block doesn't have any not visited neighbours you need to backtrack:
            a) Mark the current block as revisited.
            b) Remove a block from the stuck and make it the current block.
        5. If the current block doesn't have any not visited neighbours and the stack is empty you have reached
            the first block and visited and revisited every block. The maze has been generated. Stop iterating.
        6. Continue with next iteration."""
        neighbours = self.current_block.look_for_neighbour(self.grid)
        next_block = choice(neighbours) if neighbours else None
        if next_block:
            self.stack.push(self.current_block)
            if next_block == self.grid[-1] and not self.is_path_found:
                self.mark_blocks_as_part_of_path(next_block)
                self.is_path_found = True
            self.current_block.remove_wall_between_two_blocks(next_block)
            self.current_block = next_block
            self.current_block.visited = True
            return False
        elif not self.stack.is_empty():
            self.current_block.revisited = True
            self.current_block = self.stack.pop()
            return False
        else:
            self.current_block.revisited = True
            return True
