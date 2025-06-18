import pygame
from grid import Grid
from blocks import *
import random
import json
from colors import Colors

class Game:
    def __init__(self):
        self.grid = Grid()
        self.all_blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        random.shuffle(self.all_blocks)
        self.blocks_bag = list(self.all_blocks)
        self.current_block = self.get_next_block_from_bag()
        self.next_block = self.get_next_block_from_bag()

        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.hard_drop_points = 0
        self.combo_counter = -1

        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

        self.highscore_file = "highscores.json"
        self.highscores = self.load_highscores()

        self.held_block = None
        self.can_hold = True

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 150 * self.level
        elif lines_cleared == 2:
            self.score += 400 * self.level
        elif lines_cleared == 3:
            self.score += 700 * self.level
        elif lines_cleared == 4:
            self.score += 1200 * self.level
        self.score += move_down_points

        if lines_cleared > 0 and self.combo_counter > 0:
            combo_bonus = self.combo_counter * 50 * self.level
            self.score += combo_bonus

        self.lines_cleared_total += lines_cleared
        if self.lines_cleared_total >= self.level * 10:
            self.level += 1

    def get_next_block_from_bag(self):
        if len(self.blocks_bag) == 0:
            self.blocks_bag = list(self.all_blocks)
            random.shuffle(self.blocks_bag)
        block = self.blocks_bag.pop(0)
        block.reset_position()
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def hard_drop(self):
        initial_row = self.current_block.row_offset
        ghost_tiles = self.current_block.get_ghost_cell_positions(self.grid)
        if ghost_tiles:
            target_row_offset = ghost_tiles[0].row - self.current_block.cells[self.current_block.rotation_state][0].row
            rows_to_move = target_row_offset - initial_row
            self.current_block.move(rows_to_move, 0)
            self.hard_drop_points = rows_to_move * 2
        else:
            self.hard_drop_points = 0
        self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        self.current_block = self.next_block
        self.current_block.reset_position()

        # تحقق من ملاءمة الكتلة الجديدة قبل الاستمرار
        if not self.block_fits():
            print("Game Over: new block doesn't fit.")
            self.game_over = True
            self.update_highscores()
            return

        self.next_block = self.get_next_block_from_bag()

        rows_cleared = self.grid.clear_full_rows()

        if rows_cleared > 0:
            self.update_score(rows_cleared, 0)
            self.combo_counter += 1
        else:
            self.combo_counter = -1

        self.can_hold = True

    def reset(self):
        self.grid.reset()
        self.all_blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        random.shuffle(self.all_blocks)
        self.blocks_bag = list(self.all_blocks)
        self.current_block = self.get_next_block_from_bag()
        self.next_block = self.get_next_block_from_bag()
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.combo_counter = -1
        self.held_block = None
        self.can_hold = True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def get_drop_speed(self):
        return max(50, 200 - (self.level - 1) * 10)

    def load_highscores(self):
        try:
            with open(self.highscore_file, 'r') as f:
                scores = json.load(f)
                return sorted(scores, reverse=True)[:5]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_highscores(self):
        with open(self.highscore_file, 'w') as f:
            json.dump(self.highscores, f)

    def update_highscores(self):
        if self.score > 0:
            self.highscores.append(self.score)
            self.highscores = sorted(self.highscores, reverse=True)[:5]
            self.save_highscores()

    def hold_block(self):
        if self.can_hold:
            if self.held_block is None:
                self.held_block = self.current_block
                self.current_block = self.next_block
                self.next_block = self.get_next_block_from_bag()
            else:
                temp = self.current_block
                self.current_block = self.held_block
                self.held_block = temp

            self.current_block.reset_position()
            if not self.block_fits():
                self.game_over = True
            self.can_hold = False

    def draw(self, screen):
        self.grid.draw(screen)

        if not self.game_over:
            ghost_tiles = self.current_block.get_ghost_cell_positions(self.grid)
            for tile in ghost_tiles:
                ghost_rect = pygame.Rect(tile.column * self.current_block.cell_size + 11,
                                         tile.row * self.current_block.cell_size + 11,
                                         self.current_block.cell_size - 1, self.current_block.cell_size - 1)
                pygame.draw.rect(screen, Colors.helwan_grey_light, ghost_rect, 1)

        self.current_block.draw(screen, 11, 11)
        self.next_block.draw(screen, 320, 215, center_in_box=True)

        if self.held_block:
            self.held_block.draw(screen, 320, 400, center_in_box=True)
