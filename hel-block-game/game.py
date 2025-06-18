import pygame
from grid import Grid
from blocks import *
import random
import json
import os # <--- إضافة مهمة: استيراد مكتبة os
from colors import Colors

# --- بداية التعديل: تحديد المسار الأساسي للمشروع لملف game.py ---
# ده بيجيب المسار المطلق للمجلد اللي فيه ملف game.py
current_game_dir = os.path.dirname(os.path.abspath(__file__))
game_assets_base_path = current_game_dir
# --- نهاية التعديل ---

class Game:
    def __init__(self):
        pygame.mixer.init() 

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

        # --- التعديل هنا: استخدام os.path.join لتحميل ملفات الصوت ---
        try:
            self.rotate_sound = pygame.mixer.Sound(os.path.join(game_assets_base_path, "Sounds", "rotate.ogg"))
            self.clear_sound = pygame.mixer.Sound(os.path.join(game_assets_base_path, "Sounds", "clear.ogg"))
            pygame.mixer.music.load(os.path.join(game_assets_base_path, "Sounds", "music.ogg")) 
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Warning: Could not load sound files - {e}")
            self.rotate_sound = None
            self.clear_sound = None

        self.highscore_file = os.path.join(game_assets_base_path, "highscores.json") # <--- تعديل: تحديد مسار ملف النقاط
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
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
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
        self.next_block = self.get_next_block_from_bag()
        
        rows_cleared = self.grid.clear_full_rows() 
        
        if rows_cleared > 0:
            if self.clear_sound:
                pygame.mixer.Sound.play(self.clear_sound) 
            self.update_score(rows_cleared, 0)
            self.combo_counter += 1
        else:
            self.combo_counter = -1

        if self.block_fits() == False:
            self.game_over = True
            self.update_highscores()
        
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
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        try:
            # --- التعديل هنا: استخدام os.path.join لإعادة تشغيل الموسيقى ---
            pygame.mixer.music.load(os.path.join(game_assets_base_path, "Sounds", "music.ogg"))
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Warning: Could not restart music - {e}")

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            if self.rotate_sound:
                pygame.mixer.Sound.play(self.rotate_sound)

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def get_drop_speed(self):
        speed = max(50, 200 - (self.level - 1) * 10)
        return speed

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
            if self.held_block == None:
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

        next_block_offset_x = 320
        next_block_offset_y = 215
        
        self.next_block.draw(screen, next_block_offset_x, next_block_offset_y, center_in_box=True)

        held_block_offset_x = 320
        held_block_offset_y = 400

        if self.held_block:
            self.held_block.draw(screen, held_block_offset_x, held_block_offset_y, center_in_box=True)
