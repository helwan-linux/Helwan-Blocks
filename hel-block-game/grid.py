import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_columns = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_columns)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()
        
        # Offset for drawing the grid on the screen
        self.offset_x = 110 # كانت 20
        self.offset_y = 10 # كانت 20

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                print(self.grid[row][column], end = " ")
            print()

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(self.offset_x + column * self.cell_size, 
                                        self.offset_y + row * self.cell_size, 
                                        self.cell_size -1, self.cell_size -1) # -1 for border effect
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
    
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_columns:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def clear_full_rows(self):
        cleared_rows = 0
        rows_to_clear = []
        for row in range(self.num_rows -1, 0, -1): # ابدأ من الأسفل
            if self.is_row_full(row):
                rows_to_clear.append(row)
        
        # قم بإزالة الصفوف الممتلئة وحرك الصفوف العلوية للأسفل
        for row_to_clear in sorted(rows_to_clear, reverse=True):
            for r in range(row_to_clear, 0, -1):
                self.grid[r] = self.grid[r-1][:] # نسخ الصف العلوي
            self.grid[0] = [0 for _ in range(self.num_columns)] # إفراغ الصف العلوي

        cleared_rows = len(rows_to_clear)
        return cleared_rows

    def is_row_full(self, row):
        for column in range(self.num_columns):
            if self.grid[row][column] == 0:
                return False
        return True

    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = 0
