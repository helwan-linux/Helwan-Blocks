from grid import Grid
from blocks import *
import random
import pygame
from colors import Colors # تأكد من استيراد Colors هنا

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

        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1) # Play music indefinitely

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
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
            self.combo_counter += 1 # --- إضافة جديدة: زيادة الكومبو عند مسح صفوف
        else:
            self.combo_counter = -1 # --- إضافة جديدة: إعادة تعيين الكومبو إذا لم يتم مسح صفوف

        if self.block_fits() == False:
            self.game_over = True

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
        self.combo_counter = -1 # --- إضافة جديدة: إعادة تعيين الكومبو عند إعادة اللعب

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
            self.rotate_sound.play()

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
                # You can choose a light color from Colors or even a transparent one if Pygame supports it directly
                # For simple outline:
                pygame.draw.rect(screen, Colors.helwan_grey_light, ghost_rect, 1) # Draw outline (thickness 1)
                # Or for a slightly filled, transparent look (more complex, might need Surface with SRCALPHA)
                # For now, a simple outline is good.


        # Draw the current block
        self.current_block.draw(screen, 11, 11)

        # Adjusted Next Block positions
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255 + 50, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255 + 50, 280)
        else:
            self.next_block.draw(screen, 270 + 50, 270)
