import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()
        # --- Helwan Linux Customization: For row clear animation ---
        self.clearing_rows = [] # To store rows that are currently being cleared
        self.clear_animation_start_time = 0
        self.clear_animation_duration = 150 # Duration of the flash in milliseconds

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        rows_to_clear_now = [] # Store rows that are full in this pass

        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                rows_to_clear_now.append(row)
                completed += 1

        if completed > 0:
            self.clearing_rows = rows_to_clear_now # Store for animation
            self.clear_animation_start_time = pygame.time.get_ticks() # Start timer

            # We will delay the actual clearing and moving until after the animation
            # This is handled in the draw method based on the timer
        return completed

    def perform_actual_row_clear(self):
        """Performs the actual clearing and moving of rows after animation."""
        if not self.clearing_rows:
            return

        # Sort rows in descending order to avoid issues when moving down
        self.clearing_rows.sort(reverse=True)
        completed_count = 0
        for row in self.clearing_rows:
            self.clear_row(row)
            completed_count += 1
        
        # Now move down rows above the cleared ones
        for row_idx in range(self.clearing_rows[-1] -1, 0, -1): # Start from just above the highest cleared row
            # If the row itself was cleared, we skip it as it's already handled by clear_row
            if row_idx not in self.clearing_rows:
                # Calculate how many rows below it were cleared
                rows_moved_down = sum(1 for r in self.clearing_rows if r > row_idx)
                if rows_moved_down > 0:
                    self.move_row_down(row_idx, rows_moved_down)

        self.clearing_rows = [] # Clear the list after action

    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
        self.clearing_rows = [] # Also reset clearing animation state

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        is_animating = len(self.clearing_rows) > 0 and (current_time - self.clear_animation_start_time < self.clear_animation_duration)

        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1)

                if is_animating and row in self.clearing_rows:
                    # --- Helwan Linux Customization: Flash effect for cleared rows ---
                    # Flash with a distinct Helwan accent color
                    pygame.draw.rect(screen, Colors.helwan_green_accent, cell_rect)
                else:
                    pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
        # After drawing, if animation time has passed, perform the actual clear
        if is_animating == False and len(self.clearing_rows) > 0:
            self.perform_actual_row_clear()
