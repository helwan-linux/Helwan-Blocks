import pygame
from grid import Grid
from blocks import *
import random
import json
import os
from colors import Colors

current_game_dir = os.path.dirname(os.path.abspath(__file__))
game_assets_base_path = current_game_dir

class Game:
    def __init__(self):
        pygame.mixer.init()

        self.grid = Grid()
        self.all_blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        
        # --- تعديل هنا: التأكد من أن list(self.all_blocks) تُنشئ قائمة جديدة في كل مرة ---
        # ده بيضمن ان كيس البلوكات يتجدد دايماً
        self.blocks_bag = random.sample(self.all_blocks, k=len(self.all_blocks)) # random.sample لضمان عدم تكرار العناصر
        self.current_block = self.get_next_block_from_bag()
        self.next_block = self.get_next_block_from_bag()

        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.hard_drop_points = 0
        self.combo_counter = -1

        try:
            self.rotate_sound = pygame.mixer.Sound(os.path.join(game_assets_base_path, "Sounds", "rotate.ogg"))
            self.clear_sound = pygame.mixer.Sound(os.path.join(game_assets_base_path, "Sounds", "clear.ogg"))
            pygame.mixer.music.load(os.path.join(game_assets_base_path, "Sounds", "music.ogg"))
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Warning: Could not load sound files - {e}")
            self.rotate_sound = None
            self.clear_sound = None

        self.highscore_file = os.path.join(game_assets_base_path, "highscores.json")
        self.highscores = self.load_highscores()

        self.held_block = None
        self.can_hold = True
        self.place_new_block() # استدعاء دالة لوضع البلوك الأولي

    def place_new_block(self):
        self.current_block = self.next_block
        self.next_block = self.get_next_block_from_bag()
        # --- تعديل هنا: فحص Game Over بعد وضع البلوك الجديد ---
        if not self.block_fits_on_grid():
            self.game_over = True
            self.update_highscores()
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

    def update_score(self, lines_cleared, move_down_points):
        # النقاط الأساسية لكل سطر
        if lines_cleared == 1:
            self.score += 100 * self.level
        elif lines_cleared == 2:
            self.score += 300 * self.level
        elif lines_cleared == 3:
            self.score += 500 * self.level
        elif lines_cleared == 4: # Tetris
            self.score += 800 * self.level
        
        # نقاط السقوط اليدوي
        self.score += move_down_points
        
        # نقاط الكومبو
        if lines_cleared > 0 and self.combo_counter > 0:
            combo_bonus = self.combo_counter * 50 * self.level
            self.score += combo_bonus
        
        # نقاط الهارد دروب
        self.score += self.hard_drop_points
        self.hard_drop_points = 0 # إعادة تعيين نقاط الهارد دروب بعد إضافتها

        self.lines_cleared_total += lines_cleared
        if self.lines_cleared_total >= self.level * 10: # كل 10 سطور بيزيد الليفل
            self.level += 1
            # سرعة السقوط بتتحدث في main.py بناءً على level

    def get_next_block_from_bag(self):
        if len(self.blocks_bag) == 0:
            self.blocks_bag = random.sample(self.all_blocks, k=len(self.all_blocks)) # تجديد الكيس
        block = self.blocks_bag.pop(0)
        block.reset_position()
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits_on_grid() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits_on_grid() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits_on_grid() == False:
            self.current_block.move(-1, 0) # ارجع خطوة
            self.lock_block()

    def hard_drop(self):
        # حساب النقاط قبل القفل عشان تكون دقيقة
        rows_dropped = 0
        while True:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits_on_grid():
                self.current_block.move(-1, 0)
                break
            rows_dropped += 1
        self.hard_drop_points = rows_dropped * 2 # نقطتين لكل صف سقط
        self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        
        rows_cleared = self.grid.clear_full_rows() 
        
        if rows_cleared > 0:
            if self.clear_sound:
                pygame.mixer.Sound.play(self.clear_sound) 
            self.update_score(rows_cleared, 0)
            self.combo_counter += 1
        else:
            self.combo_counter = -1
        
        self.place_new_block() # هنا بنحط البلوك الجديد وبنفحص الـ Game Over
        self.can_hold = True

    def reset(self):
        self.grid.reset()
        self.all_blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.blocks_bag = random.sample(self.all_blocks, k=len(self.all_blocks)) # تجديد الكيس
        self.current_block = self.get_next_block_from_bag()
        self.next_block = self.get_next_block_from_bag()
        
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.combo_counter = -1
        self.held_block = None
        self.can_hold = True
        self.hard_drop_points = 0 # reset hard drop points
        self.game_over = False # إعادة تعيين حالة اللعبة

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(os.path.join(game_assets_base_path, "Sounds", "music.ogg"))
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Warning: Could not restart music - {e}")
        
        # فحص مباشر بعد الريسيت لو البلوك الجديد مش مناسب
        if not self.block_fits_on_grid():
            self.game_over = True
            self.update_highscores()


    def block_fits_on_grid(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            # --- تعديل هنا: التأكد من أن الكتل داخل الحدود ولا تصطدم بكتل موجودة ---
            if not self.grid.is_inside(tile.row, tile.column) or not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits_on_grid() == False:
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
        # سرعة السقوط تعتمد على المستوى، كل ما زاد المستوى السرعة بتزيد
        # القيم دي ممكن تحتاج تظبيط
        speed = max(50, 800 - (self.level - 1) * 60) # كانت 200 - (self.level - 1) * 10
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
            # --- تعديل هنا: فحص الـ Game Over بعد الـ Hold لو البلوك الجديد مش مناسب ---
            if not self.block_fits_on_grid():
                 self.game_over = True
            
            self.can_hold = False

    def draw(self, screen):
        self.grid.draw(screen)

        if not self.game_over:
            ghost_tiles = self.current_block.get_ghost_cell_positions(self.grid)
            for tile in ghost_tiles:
                ghost_rect = pygame.Rect(tile.column * self.current_block.cell_size + self.grid.offset_x + 1,
                                         tile.row * self.current_block.cell_size + self.grid.offset_y + 1,
                                         self.current_block.cell_size - 1, self.current_block.cell_size - 1)
                pygame.draw.rect(screen, Colors.helwan_grey_light, ghost_rect, 1)

        self.current_block.draw(screen, self.grid.offset_x, self.grid.offset_y)

        next_block_offset_x = 320
        next_block_offset_y = 215
        
        self.next_block.draw(screen, next_block_offset_x, next_block_offset_y, center_in_box=True)

        held_block_offset_x = 320
        held_block_offset_y = 400

        if self.held_block:
            self.held_block.draw(screen, held_block_offset_x, held_block_offset_y, center_in_box=True)
