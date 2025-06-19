import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

        # For row clear animation
        self.clearing_rows = []
        self.clear_animation_start_time = 0
        self.clear_animation_duration = 150  # milliseconds

    def print_grid(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))

    def is_inside(self, row, col):
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def is_empty(self, row, col):
        return self.grid[row][col] == 0

    def is_row_full(self, row):
        return all(self.grid[row][col] != 0 for col in range(self.num_cols))

    def clear_row(self, row):
        for col in range(self.num_cols):
            self.grid[row][col] = 0

    def move_row_down(self, row, num_rows):
        for col in range(self.num_cols):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_full_rows(self):
        completed = 0
        rows_to_clear_now = []

        for row in range(self.num_rows - 1, -1, -1):
            if self.is_row_full(row):
                rows_to_clear_now.append(row)
                completed += 1

        if completed > 0:
            self.clearing_rows = rows_to_clear_now
            self.clear_animation_start_time = pygame.time.get_ticks()

        return completed

    def perform_actual_row_clear(self):
        if not self.clearing_rows:
            return

        self.clearing_rows.sort(reverse=True)

        for row in self.clearing_rows:
            self.clear_row(row)

        for row_idx in range(self.clearing_rows[-1] - 1, -1, -1):
            rows_moved_down = sum(1 for r in self.clearing_rows if r > row_idx)
            if rows_moved_down > 0:
                self.move_row_down(row_idx, rows_moved_down)

        self.clearing_rows = []

    def reset(self):
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.clearing_rows = []

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        is_animating = len(self.clearing_rows) > 0 and (current_time - self.clear_animation_start_time < self.clear_animation_duration)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]

                if is_animating and row in self.clearing_rows:
                    # Blink animation for clearing rows
                    if (current_time // 150) % 2 == 0:
                        color = Colors.helwan_green_accent
                    else:
                        color = Colors.helwan_grey_light
                else:
                    color = self.colors[cell_value]

                cell_rect = pygame.Rect(col * self.cell_size + 11, row * self.cell_size + 11, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, color, cell_rect)

        if not is_animating and self.clearing_rows:
            self.perform_actual_row_clear()
