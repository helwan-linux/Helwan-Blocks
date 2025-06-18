from colors import Colors
import pygame
from position import Position

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    # --- Helwan Linux Customization: Added get_ghost_cell_positions method ---
    def get_ghost_cell_positions(self, grid):
        # Temporarily move the block down to find its lowest possible position
        original_row_offset = self.row_offset
        original_column_offset = self.column_offset

        # Simulate moving down until it hits something
        while True:
            self.row_offset += 1 # Move down one row
            # Check if block is inside and fits
            current_tiles = self.get_cell_positions()
            fits = True
            for tile in current_tiles:
                if not grid.is_inside(tile.row, tile.column) or not grid.is_empty(tile.row, tile.column):
                    fits = False
                    break
            
            if not fits:
                self.row_offset -= 1 # Move back up one step
                break

        ghost_tiles = self.get_cell_positions() # Get positions at the lowest point

        # Reset block to its original position
        self.row_offset = original_row_offset
        self.column_offset = original_column_offset

        return ghost_tiles


    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                offset_y + tile.row * self.cell_size, self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def reset_position(self):
        self.row_offset = 0
        self.column_offset = 3 # Default spawn to center (column 3, can be adjusted)
