import pygame
import numpy as np
import random

class GameOfLife:
    def __init__(self, width, height, cell_size=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.grid = np.random.randint(0, 2, (self.rows, self.cols))
        self.update_counter = 0

    def update(self):
        self.update_counter += 1
        if self.update_counter >= 10:  # Adjust this value to control the update frequency
            self.update_counter = 0
            new_grid = self.grid.copy()
            for i in range(self.rows):
                for j in range(self.cols):
                    total = self.get_neighbours(i, j)
                    if self.grid[i, j] == 1:
                        if total < 2 or total > 3:
                            new_grid[i, j] = 0
                    else:
                        if total == 3:
                            new_grid[i, j] = 1
            self.grid = new_grid

    def get_neighbours(self, row, col):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                row_edge = (row + i) % self.rows
                col_edge = (col + j) % self.cols
                total += self.grid[row_edge, col_edge]
        total -= self.grid[row, col]
        return total

    def draw(self, screen):
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                if self.grid[y, x] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, (20, 20, 20), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def spawn_cells(self, n_clumps, clump_size=8):
        for _ in range(n_clumps):
            clump_center_x = random.randint(0, self.cols - 1)
            clump_center_y = random.randint(0, self.rows - 1)

            for _ in range(clump_size):
                offset_x = random.randint(-1, 1)
                offset_y = random.randint(-1, 1)

                cell_x = (clump_center_x + offset_x) % self.cols
                cell_y = (clump_center_y + offset_y) % self.rows

                self.grid[cell_y, cell_x] = 1

