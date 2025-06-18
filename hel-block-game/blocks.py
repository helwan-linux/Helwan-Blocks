import pygame
from position import Position
from colors import Colors 

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        
        self.colors = Colors.get_cell_colors
        
        self.is_falling = True

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
        # هنا مش بنستخدم get_cell_positions() عشان الـ offsets عشان دي للرسم
        # الأوفسيتس بتاعة الحركة (row_offset, column_offset) هتستخدم فقط مع الشبكة الرئيسية
        
        # --- بداية التعديل: تبسيط حسابات المنتصف ---
        adjusted_offset_x = offset_x
        adjusted_offset_y = offset_y

        if center_in_box:
            # هنحسب أبعاد البلوك الفعلي في حالته الحالية
            current_shape_cells = self.cells[self.rotation_state]
            min_col = min(p.column for p in current_shape_cells)
            max_col = max(p.column for p in current_shape_cells)
            min_row = min(p.row for p in current_shape_cells)
            max_row = max(p.row for p in current_shape_cells)

            block_pixel_width = (max_col - min_col + 1) * self.cell_size
            block_pixel_height = (max_row - min_row + 1) * self.cell_size

            # الأبعاد الثابتة للصندوق اللي بنرسم فيه (من main.py)
            box_width = 170
            box_height = 120 # لأغلب البلوكات، كفاية 4 خلايا 4*30=120

            # حساب المسافة الإضافية لمنتصف البلوك داخل الصندوق
            # بنطرح min_col و min_row عشان نخلي بداية البلوك هي (0,0) جوه الصندوق الافتراضي
            adjusted_offset_x += (box_width - block_pixel_width) // 2 - (min_col * self.cell_size)
            adjusted_offset_y += (box_height - block_pixel_height) // 2 - (min_row * self.cell_size)
        # --- نهاية التعديل ---

        for tile_pos in self.cells[self.rotation_state]:
            # هنا بنستخدم tile_pos.column و tile_pos.row مباشرة لأن adjusted_offset_x/y already include the block's current position
            tile_rect = pygame.Rect(adjusted_offset_x + tile_pos.column * self.cell_size, 
                                    adjusted_offset_y + tile_pos.row * self.cell_size, 
                                    self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def reset_position(self):
        # --- تعديل هنا: قيم ثابتة ومجربة لمنتصف الشبكة الرئيسية ---
        self.row_offset = 0
        if self.id == 1: # IBlock
            self.column_offset = 3 # IBlock 4 خلايا عرض
        elif self.id == 4: # OBlock
            self.column_offset = 4 # OBlock 2 خلايا عرض
        else: # باقي القطع (3 خلايا عرض)
            self.column_offset = 3 
        
        self.rotation_state = 0
    
    def get_ghost_cell_positions(self, grid):
        current_tiles = self.get_cell_positions()
        original_row_offset = self.row_offset

        rows_to_fall = 0
        # هنا بنحرك البلوك فعلياً عشان نحسب موضع الشبح
        while True:
            self.row_offset += 1
            if not self.block_fits(grid): # استخدام block_fits() الخاص بالبلوك نفسه
                self.row_offset -= 1 # ارجع خطوة للخلف
                break
            rows_to_fall += 1
        
        ghost_tiles = self.get_cell_positions()
        self.row_offset = original_row_offset # ارجع البلوك لموضعه الأصلي بعد حساب الشبح

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
