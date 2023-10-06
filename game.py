import pygame
import os

from grid_block.block import Block
from maze_building.build_dfs import RandomizedDepthFirstSearch
from maze_solving.dfs import DepthFirstSearch
from maze_solving.bfs import BreadthFirstSearch
from maze_solving.a_star import AStar

OFFSET_X, OFFSET_Y = 10, 10  # To offset the whole grid by x and y pixels.
BLOCK_SIZE = 40  # Size of a grid block.
GRID_COLUMNS, GRID_ROWS = 30, 20  # Number of columns and rows of a generated grid.


class Game:
    def __init__(self):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        pygame.display.set_caption("Maze")
        pygame_icon = pygame.image.load("maze_icon.png")
        pygame.display.set_icon(pygame_icon)
        self.window_size = (screen_width - 10, screen_height - 50)
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.run = True
        self.clock = pygame.time.Clock()

        self.grid = None
        self.show_visited_revisited = True  # Used when generating and solving a maze to visualise process
        self.show_path = False  # Used to show/hide the shortest path created when building a maze
        self.is_grid_created = False
        self.is_maze_generated = False
        self.chosen_solving_algorithm = None
        self.algorithm = None
        self.iteration_counter = 0

    def create_grid(self, number_of_columns=10, number_of_rows=10):
        self.grid = [Block(x, y) for y in range(number_of_rows) for x in range(number_of_columns)]

    def mark_block_as_visited_revisited_or_part_of_path(self, block):
        circle_x = block.x_index * BLOCK_SIZE + OFFSET_X + BLOCK_SIZE / 2
        circle_y = block.y_index * BLOCK_SIZE + OFFSET_Y + BLOCK_SIZE / 2

        if block.part_of_path and self.show_path:
            pygame.draw.circle(self.window, "white", (circle_x, circle_y), BLOCK_SIZE / 4)
        elif block.revisited and self.show_visited_revisited:
            pygame.draw.circle(self.window, "green", (circle_x, circle_y), BLOCK_SIZE / 4)
        elif block.visited and self.show_visited_revisited:
            pygame.draw.circle(self.window, "orange", (circle_x, circle_y), BLOCK_SIZE / 4)

    def draw_grid(self, grid):
        for block in grid:
            top_left_corner = (block.x_index * BLOCK_SIZE + OFFSET_X,
                               block.y_index * BLOCK_SIZE + OFFSET_Y)
            top_right_corner = (block.x_index * BLOCK_SIZE + OFFSET_X + BLOCK_SIZE,
                                block.y_index * BLOCK_SIZE + OFFSET_Y)
            bottom_left_corner = (block.x_index * BLOCK_SIZE + OFFSET_X,
                                  block.y_index * BLOCK_SIZE + OFFSET_Y + BLOCK_SIZE)
            bottom_right_corner = (block.x_index * BLOCK_SIZE + OFFSET_X + BLOCK_SIZE,
                                   block.y_index * BLOCK_SIZE + OFFSET_Y + BLOCK_SIZE)
            if block.wall.n:
                pygame.draw.line(self.window, "orange", top_left_corner, top_right_corner, 1)
            if block.wall.e:
                pygame.draw.line(self.window, "orange", top_right_corner, bottom_right_corner, 1)
            if block.wall.s:
                pygame.draw.line(self.window, "orange", bottom_right_corner, bottom_left_corner, 1)
            if block.wall.w:
                pygame.draw.line(self.window, "orange", bottom_left_corner, top_left_corner, 1)

            if self.show_visited_revisited or self.show_path:
                self.mark_block_as_visited_revisited_or_part_of_path(block)

    def clear_screen(self):
        self.window.fill("black")

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Show/hide the shortest path
                    self.show_path = not self.show_path
                elif event.key == pygame.K_SPACE:  # Show/hide visualization when building or solving a maze
                    self.show_visited_revisited = not self.show_visited_revisited
                elif event.key == pygame.K_ESCAPE:  # Hide the shortest path and building/solving visualization
                    self.show_path = False
                    self.show_visited_revisited = False
                elif event.key == pygame.K_g:  # Generate a new maze
                    self.is_grid_created = False
                    self.is_maze_generated = False
                elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                    # Use DFS/BSF/A* algorithm to solve a maze
                    if self.is_maze_generated and self.algorithm is None:
                        event_key_map = {49: "DFS", 50: "BFS", 51: "A*"}
                        self.show_visited_revisited = True
                        self.chosen_solving_algorithm = event_key_map[event.key]
            elif event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.VIDEORESIZE:
                self.window_size = event.size
                self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

    def assign_chosen_solving_algorithm(self):
        if self.chosen_solving_algorithm == "DFS":
            self.algorithm = DepthFirstSearch(self.grid, self.grid[0], self.grid[-1])
        elif self.chosen_solving_algorithm == "BFS":
            self.algorithm = BreadthFirstSearch(self.grid, self.grid[0], self.grid[-1])
        else:  # self.chosen_solving_algorithm == "A*"
            self.algorithm = AStar(self.grid, self.grid[0], self.grid[-1])

    def game_loop(self):
        self.clock.tick(60)
        build_dfs = None

        while self.run:
            # pygame.time.delay(100)
            self.clear_screen()
            if not self.is_grid_created:    # Runs when a grid needs to be created
                self.create_grid(GRID_COLUMNS, GRID_ROWS)
                build_dfs = RandomizedDepthFirstSearch(self.grid)
                self.is_grid_created = True
            self.draw_grid(self.grid)
            if not self.is_maze_generated:  # Runs when a maze needs to be generated
                self.is_maze_generated = build_dfs.iterate()
            elif self.chosen_solving_algorithm is not None:  # Runs when a maze needs to be solved
                if self.algorithm is None:
                    self.assign_chosen_solving_algorithm()
                is_maze_solved = self.algorithm.iterate()
                self.iteration_counter += 1
                if is_maze_solved:
                    print(f"The maze was solved by {self.chosen_solving_algorithm} in {self.iteration_counter} steps.")
                    self.chosen_solving_algorithm = None
                    self.algorithm = None
                    self.iteration_counter = 0
            self.check_events()
            pygame.display.update()
        pygame.quit()
