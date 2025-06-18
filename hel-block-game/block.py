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
        
        adjusted_offset_x = offset_x
        adjusted_offset_y = offset_y

        if center_in_box:
            # --- بداية التعديل هنا: حسابات دقيقة للمنتصف في الصندوق الجانبي ---
            # حساب أقصى وأدنى إحداثيات للكتلة في حالتها الحالية
            min_row = min(p.row for p in self.cells[self.rotation_state])
            max_row = max(p.row for p in self.cells[self.rotation_state])
            min_col = min(p.column for p in self.cells[self.rotation_state])
            max_col = max(p.column for p in self.cells[self.rotation_state])

            block_width_cells = max_col - min_col + 1
            block_height_cells = max_row - min_row + 1

            # حجم الصندوق اللي بنرسم جواه القطعة (مثلاً، 4x4 خلايا عشان يستوعب أكبر قطعة وهي I)
            # بما إن الـ cell_size = 30، يبقى الصندوق 4*30 = 120 بكسل
            # الصناديق في main.py هي 170x120، يبقى عندنا 120 بكسل عرض لرسم القطعة
            # بما إن الـ cell_size = 30، الـ 120 بكسل بتكفي 4 خلايا.
            # هنجرب نخلي ابعاد الصندوق الافتراضية 4x4 خلايا لتحديد المنتصف
            box_width_cells_for_centering = 4
            box_height_cells_for_centering = 4
            
            # حساب الإزاحة المطلوبة لمنتصف الكتلة داخل صندوق بحجم 4x4 خلايا
            # دي بتشيل الـ offset الداخلي للقطعة نفسها
            center_x_offset_cells = (box_width_cells_for_centering - block_width_cells) / 2 - min_col
            center_y_offset_cells = (box_height_cells_for_centering - block_height_cells) / 2 - min_row

            # تحويل الإزاحة من خلايا إلى بكسل وإضافتها للـ offset الأساسي
            adjusted_offset_x = offset_x + center_x_offset_cells * self.cell_size
            adjusted_offset_y = offset_y + center_y_offset_cells * self.cell_size
            # --- نهاية التعديل ---

        for tile_pos in self.cells[self.rotation_state]: # نستخدم self.cells مباشرة هنا
            tile_rect = pygame.Rect(adjusted_offset_x + tile_pos.column * self.cell_size, 
                                    adjusted_offset_y + tile_pos.row * self.cell_size, 
                                    self.cell_size -1, self.cell_size -1) # -1 for border effect
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def reset_position(self):
        self.row_offset = 0
        self.column_offset = 3 # كانت 0، هنجرب 3 أو 4 لمنتصف الشبكة الرئيسية

        # بعض القطع بتحتاج row_offset مختلف عشان تكون في أول الشبكة صح
        if self.id == 3: # LBlock (مثلاً)
            self.column_offset = 3
        elif self.id == 4: # OBlock
            self.column_offset = 4
        elif self.id == 1: # IBlock
             self.column_offset = 3
        else: # باقي القطع
             self.column_offset = 3
        
        self.rotation_state = 0
    
    def get_ghost_cell_positions(self, grid):
        current_tiles = self.get_cell_positions()
        original_row_offset = self.row_offset

        # Find how many rows down the block can fall
        rows_to_fall = 0
        while True:
            self.row_offset += 1
            if not grid.is_inside(current_tiles[0].row + self.row_offset, current_tiles[0].column + self.column_offset) or not self.block_fits(grid): # استخدام tile.row و tile.column في الكود الأصلي كان بيسبب مشكلة
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
            # --- تعديل هنا: التأكد من أن الكتل داخل الحدود ولا تصطدم بكتل موجودة ---
            if not grid.is_inside(tile.row, tile.column) or not grid.is_empty(tile.row, tile.column):
                return False
        return True
