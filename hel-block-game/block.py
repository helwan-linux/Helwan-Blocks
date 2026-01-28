from colors import Colors
import pygame
from position import Position

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = -1
        self.column_offset = 3  # بداية مناسبة داخل الشبكة
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            moved_tiles.append(Position(position.row + self.row_offset, position.column + self.column_offset))
        return moved_tiles

    def get_ghost_cell_positions(self, grid):
        original_row_offset = self.row_offset
        while True:
            self.row_offset += 1
            current_tiles = self.get_cell_positions()
            fits = True
            for tile in current_tiles:
                if not grid.is_inside(tile.row, tile.column) or not grid.is_empty(tile.row, tile.column):
                    fits = False
                    break
            if not fits:
                self.row_offset -= 1
                break
        ghost_tiles = self.get_cell_positions()
        self.row_offset = original_row_offset
        return ghost_tiles

    def rotate(self):
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)

    def undo_rotation(self):
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)

    def draw(self, screen, offset_x, offset_y, center_in_box=False, box_width=170, box_height=180):
        tiles = self.get_cell_positions()
        if center_in_box:
            min_row = min(tile.row for tile in tiles)
            max_row = max(tile.row for tile in tiles)
            min_col = min(tile.column for tile in tiles)
            max_col = max(tile.column for tile in tiles)

            block_width_cells = max_col - min_col + 1
            block_height_cells = max_row - min_row + 1

            block_pixel_width = block_width_cells * self.cell_size
            block_pixel_height = block_height_cells * self.cell_size

            target_grid_size_pixels = 4 * self.cell_size

            center_offset_x = (target_grid_size_pixels - block_pixel_width) // 2
            center_offset_y = (target_grid_size_pixels - block_pixel_height) // 2

            draw_offset_x = offset_x + center_offset_x - (min_col * self.cell_size)
            draw_offset_y = offset_y + center_offset_y - (min_row * self.cell_size)
        else:
            draw_offset_x = offset_x
            draw_offset_y = offset_y

        for tile in tiles:
            tile_rect = pygame.Rect(draw_offset_x + tile.column * self.cell_size,
                                    draw_offset_y + tile.row * self.cell_size,
                                    self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def reset_position(self):
        self.row_offset = 0
        self.column_offset = 3
