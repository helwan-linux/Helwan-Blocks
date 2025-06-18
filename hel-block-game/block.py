import pygame
from position import Position
from colors import Colors # تأكد أن Colors مستوردة

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        
        # --- التعديل هنا: إزالة الأقواس () من Colors.get_cell_colors ---
        self.colors = Colors.get_cell_colors
        
        self.is_falling = True # Add a flag to track if the block is still falling

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            moved_tiles.append(Position(position.row + self.row_offset, position.column + self.column_offset))
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x=0, offset_y=0, center_in_box=False):
        tiles = self.get_cell_positions()
        
        # Calculate bounding box for centering
        min_row = min(p.row for p in tiles)
        max_row = max(p.row for p in tiles)
        min_col = min(p.column for p in tiles)
        max_col = max(p.column for p in tiles)

        block_width_cells = max_col - min_col + 1
        block_height_cells = max_row - min_row + 1

        # Adjust offsets if centering is requested
        if center_in_box:
            # Assuming a fixed box size for next/held blocks (e.g., 4 cells wide for centering)
            box_width_cells = 5 # A bit larger to give space, or whatever fits your UI boxes
            box_height_cells = 5 # Same here

            center_x_offset = (box_width_cells - block_width_cells) / 2 - min_col # Adjust for block's internal offset
            center_y_offset = (box_height_cells - block_height_cells) / 2 - min_row # Adjust for block's internal offset

            adjusted_offset_x = offset_x + center_x_offset * self.cell_size
            adjusted_offset_y = offset_y + center_y_offset * self.cell_size
        else:
            adjusted_offset_x = offset_x
            adjusted_offset_y = offset_y


        for tile in tiles:
            tile_rect = pygame.Rect(adjusted_offset_x + tile.column * self.cell_size, 
                                    adjusted_offset_y + tile.row * self.cell_size, 
                                    self.cell_size -1, self.cell_size -1) # -1 for border effect
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def reset_position(self):
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
    
    def get_ghost_cell_positions(self, grid):
        current_tiles = self.get_cell_positions()
        original_row_offset = self.row_offset

        # Find how many rows down the block can fall
        rows_to_fall = 0
        while True:
            self.row_offset += 1
            if not self.block_fits(grid):
                self.row_offset -= 1 # Move back to the last valid position
                break
            rows_to_fall += 1
        
        ghost_tiles = self.get_cell_positions()
        self.row_offset = original_row_offset # Reset to original position

        # Return only if the block can actually fall further than its current position
        if rows_to_fall > 0:
            return ghost_tiles
        return []

    def block_fits(self, grid):
        tiles = self.get_cell_positions()
        for tile in tiles:
            if not grid.is_inside(tile.row, tile.column) or not grid.is_empty(tile.row, tile.column):
                return False
        return True
