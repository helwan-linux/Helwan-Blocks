import pygame
from grid import Grid
from blocks import *
import random
import json # استيراد مكتبة json لحفظ وتحميل النقاط
from colors import Colors # تأكد من استيراد Colors

class Game:
    def __init__(self):
        self.grid = Grid()
        # --- Helwan Linux Customization: Implementing The Bag Theory for block generation ---
        self.all_blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        random.shuffle(self.all_blocks) # Shuffle the "bag"
        self.blocks_bag = list(self.all_blocks) # Create the first bag
        self.current_block = self.get_next_block_from_bag()
        self.next_block = self.get_next_block_from_bag()

        self.game_over = False
        self.score = 0
        self.level = 1 # Added game levels
        self.lines_cleared_total = 0 # To track total lines for level progression
        self.hard_drop_points = 0 # Initialize hard drop points
        self.combo_counter = -1 # --- إضافة جديدة: عداد الكومبو. -1 يشير إلى عدم وجود كومبو حالي.

        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        #pygame.mixer.music.load("Sounds/music.ogg") # تم تعطيل الصوتيات بناءً على طلبك
        #pygame.mixer.music.play(-1) # Play music indefinitely

        # --- Helwan Linux Customization: High Score related variables ---
        self.highscore_file = "highscores.json"
        self.highscores = self.load_highscores()

        # --- Helwan Linux Customization: Hold Piece variables ---
        self.held_block = None       # Stores the block currently being held
        self.can_hold = True         # Flag to prevent multiple holds per turn

    # --- Helwan Linux Customization: Modified Score System ---
    # More unique scoring, including a simple multiplier.
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 150 * self.level
        elif lines_cleared == 2:
            self.score += 400 * self.level
        elif lines_cleared == 3:
            self.score += 700 * self.level
        elif lines_cleared == 4: # Tetris!
            self.score += 1200 * self.level
            # Add a visual/audio cue for Tetris clear, specific to Helwan Linux.
        self.score += move_down_points

        # --- إضافة جديدة: نقاط الكومبو ---
        if lines_cleared > 0 and self.combo_counter > 0: # إذا مسح صفوف وكان هناك كومبو سابق
            combo_bonus = self.combo_counter * 50 * self.level # نقاط إضافية بناءً على عدد الكومبو
            self.score += combo_bonus
            # يمكنك إضافة تأثير بصري أو صوتي هنا للكومبو!
        
        # Update total lines cleared and check for level up
        self.lines_cleared_total += lines_cleared
        if self.lines_cleared_total >= self.level * 10: # Advance level every 10 lines (can be adjusted)
            self.level += 1
            # سرعة السقوط سيتم تعديلها في مكان آخر عند زيادة المستوى (في main.py)

    # --- Helwan Linux Customization: Bag Theory Implementation ---
    def get_next_block_from_bag(self):
        if len(self.blocks_bag) == 0:
            self.blocks_bag = list(self.all_blocks)
            random.shuffle(self.blocks_bag)
        block = self.blocks_bag.pop(0) # Get the first block from the shuffled bag
        block.reset_position() # Ensure block starts from its initial position (now available in Block class)
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

    # --- Helwan Linux Customization: Hard Drop Feature ---
    # Allows block to instantly drop to the bottom
    def hard_drop(self):
        initial_row = self.current_block.row_offset
        # Use a temporary position for hard drop calculation without affecting current block
        # The get_ghost_cell_positions method already handles this logic to find the drop point
        ghost_tiles = self.current_block.get_ghost_cell_positions(self.grid)
        
        # Calculate how many rows to move down based on ghost position
        # Assuming all tiles in ghost_tiles have the same row offset relative to the block's top-left cell
        # We need to find the effective row offset for the block itself
        if ghost_tiles:
            target_row_offset = ghost_tiles[0].row - self.current_block.cells[self.current_block.rotation_state][0].row
            rows_to_move = target_row_offset - initial_row
            self.current_block.move(rows_to_move, 0)
            self.hard_drop_points = rows_to_move * 2 # Points based on distance
        else: # Should not happen if game is designed correctly, but for safety
            self.hard_drop_points = 0


        self.lock_block()


    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_next_block_from_bag()
        
        # Call clear_full_rows, which now initiates animation.
        # The actual clear happens in Grid.draw() after animation.
        rows_cleared = self.grid.clear_full_rows() 
        
        if rows_cleared > 0:
            #pygame.mixer.Sound.play(self.clear_sound) # Disable sound for now
            self.update_score(rows_cleared, 0)
            self.combo_counter += 1 # --- إضافة جديدة: زيادة الكومبو عند مسح صفوف
        else:
            self.combo_counter = -1

        if self.block_fits() == False:
            self.game_over = True
            self.update_highscores() # --- إضافة جديدة: تحديث أعلى النقاط عند نهاية اللعبة
        
        self.can_hold = True # --- إضافة جديدة: يمكن اللاعب الحفظ مرة أخرى بعد تثبيت الكتلة

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
        self.held_block = None       # --- إضافة جديدة: إعادة تعيين قطعة الاحتفاظ
        self.can_hold = True         # --- إضافة جديدة: إعادة تعيين إمكانية الحفظ

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
            #pygame.mixer.Sound.play(self.rotate_sound) # Disable sound for now
            pass # Keep rotate sound functionality but disable actual playback for now

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    # --- إضافة جديدة: دالة لحساب سرعة السقوط بناءً على المستوى ---
    def get_drop_speed(self):
        # كلما زاد المستوى، قلت المدة الزمنية، وبالتالي تزداد السرعة
        # 200 مللي ثانية في المستوى الأول، ثم تقل تدريجياً
        speed = max(50, 200 - (self.level - 1) * 10) # لا تقل عن 50 مللي ثانية
        return speed

    # --- Helwan Linux Customization: High Score Methods ---
    def load_highscores(self):
        try:
            with open(self.highscore_file, 'r') as f:
                scores = json.load(f)
                # Ensure scores are sorted descending and take only top 5 (or desired number)
                return sorted(scores, reverse=True)[:5]
        except (FileNotFoundError, json.JSONDecodeError):
            return [] # Return empty list if file not found or corrupted

    def save_highscores(self):
        with open(self.highscore_file, 'w') as f:
            json.dump(self.highscores, f)

    def update_highscores(self):
        # Only add score if it's not 0 (e.g., from game over immediately)
        if self.score > 0:
            self.highscores.append(self.score)
            self.highscores = sorted(self.highscores, reverse=True)[:5] # Keep top 5 scores
            self.save_highscores() # Save to file

    # --- Helwan Linux Customization: Hold Block Method ---
    def hold_block(self):
        if self.can_hold:
            if self.held_block == None: # If nothing is held, just hold the current block
                self.held_block = self.current_block
                self.current_block = self.next_block
                self.next_block = self.get_next_block_from_bag()
            else: # If a block is already held, swap it with the current block
                temp = self.current_block
                self.current_block = self.held_block
                self.held_block = temp
            
            # Reset position of the block coming into play
            self.current_block.reset_position() 
            # Check if new block can fit, if not, it's game over (unlikely for new blocks)
            if not self.block_fits():
                 self.game_over = True # Should ideally not happen with proper spawn.
            
            self.can_hold = False # Player cannot hold again until block is locked
            
            # --- إضافة جديدة: تحديث الشاشة فوراً بعد التبديل لسرعة الاستجابة ---
            # بما أن دالة main.py تقوم باستدعاء game.draw(screen) في كل لفة
            # وهذا يتم تحديثه بواسطة pygame.display.update()، فإن التحديث سيكون سريعاً بما فيه الكفاية.
            # لا حاجة لإضافة تحديث هنا.


    def draw(self, screen):
        self.grid.draw(screen) # Draw the grid first

        # --- Helwan Linux Customization: Draw Ghost Piece ---
        # Draw ghost piece only if game is not over
        if not self.game_over:
            ghost_tiles = self.current_block.get_ghost_cell_positions(self.grid)
            for tile in ghost_tiles:
                # Draw with a lighter color or just an outline
                ghost_rect = pygame.Rect(tile.column * self.current_block.cell_size + 11,
                                         tile.row * self.current_block.cell_size + 11,
                                         self.current_block.cell_size - 1, self.current_block.cell_size - 1)
                # For simple outline:
                pygame.draw.rect(screen, Colors.helwan_grey_light, ghost_rect, 1) # Draw outline (thickness 1)


        # Draw the current block
        self.current_block.draw(screen, 11, 11)

        # --- تعديل: إحداثيات رسم "Next Block" (القطعة التالية) ---
        next_block_offset_x = 320 # بداية صندوق Next Block
        next_block_offset_y = 215 # بداية صندوق Next Block
        
        # استدعاء دالة draw في Block مع تفعيل center_in_box=True
        # الآن Block هو المسؤول عن توسيط نفسه داخل المساحة
        self.next_block.draw(screen, next_block_offset_x, next_block_offset_y, center_in_box=True)

        # --- تعديل: إحداثيات رسم "Held Block" (القطعة المحفوظة) ---
        held_block_offset_x = 320 # بداية صندوق Held Block
        held_block_offset_y = 400 # بداية صندوق Held Block

        if self.held_block:
            # استدعاء دالة draw في Block مع تفعيل center_in_box=True
            self.held_block.draw(screen, held_block_offset_x, held_block_offset_y, center_in_box=True)
