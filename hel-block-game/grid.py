import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors
        self.cleared_rows = []
        self.clear_animation_frames = 10
        self.current_animation_frame = 0

        # Offset للشبكة عشان تكون في منتصف الشاشة تقريباً
        self.offset_x = 11 # القيمة دي ممكن تحتاج تظبيط بسيط عشان تكون في المنتصف
        self.offset_y = 11 # القيمة دي ممكن تحتاج تظبيط بسيط عشان تكون في المنتصف


    def print_grid(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end = " ")
            print()

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def def clear_full_rows(self): # <--- فيه غلطة هنا
        cleared = 0
        self.cleared_rows = []
        for row in range(self.num_rows -1, 0, -1):
            if self.is_row_full(row):
                self.cleared_rows.append(row)
                self.clear_row(row)
                cleared += 1
        return cleared

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_rows_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                # --- التعديل هنا: استخدام offset_x و offset_y لضبط مكان الرسم ---
                cell_rect = pygame.Rect(column * self.cell_size + self.offset_x,
                                        row * self.cell_size + self.offset_y,
                                        self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
        
        # رسم الحدود الخارجية للشبكة
        border_rect = pygame.Rect(self.offset_x - 1, self.offset_y - 1,
                                  self.num_cols * self.cell_size + 2, # +2 للحدود
                                  self.num_rows * self.cell_size + 2) # +2 للحدود
        pygame.draw.rect(screen, Colors.black, border_rect, 2) # رسم حدود سوداء سمكها 2 بكسل

        if self.cleared_rows:
            self.current_animation_frame += 1
            if self.current_animation_frame < self.clear_animation_frames:
                for r_index in self.cleared_rows:
                    animation_color = (255, 255, 255)
                    # --- التعديل هنا: استخدام offset_x و offset_y للحركة ---
                    animation_rect = pygame.Rect(self.offset_x, r_index * self.cell_size + self.offset_y,
                                                self.num_cols * self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, animation_color, animation_rect)
            else:
                for r_index in sorted(self.cleared_rows, reverse=True):
                    for row_to_move in range(r_index - 1, -1, -1):
                        self.move_rows_down(row_to_move, 1)
                self.cleared_rows = []
                self.current_animation_frame = 0
