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

    def get_ghost_cell_positions(self, grid):
        original_row_offset = self.row_offset
        original_column_offset = self.column_offset

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

    # --- تعديل كبير هنا: دالة الرسم مع دعم التوسيط ---
    def draw(self, screen, offset_x, offset_y, center_in_box=False, box_width=170, box_height=180):
        tiles = self.get_cell_positions()
        
        # إذا طلبنا التوسيط داخل صندوق معين
        if center_in_box:
            # ابحث عن الحد الأدنى والأقصى للصفوف والأعمدة للكتلة في حالتها ودورانها الحاليين
            min_row = min([tile.row for tile in tiles])
            max_row = max([tile.row for tile in tiles])
            min_col = min([tile.column for tile in tiles])
            max_col = max([tile.column for tile in tiles])

            # أبعاد الكتلة بالخلايا (عرض الخلايا وارتفاعها)
            block_width_cells = max_col - min_col + 1
            block_height_cells = max_row - min_row + 1

            # الحجم الفعلي للكتلة بالبكسل
            block_pixel_width = block_width_cells * self.cell_size
            block_pixel_height = block_height_cells * self.cell_size

            # حساب الإزاحة لتوسيط الكتلة داخل منطقة افتراضية بحجم 4x4 خلايا (120x120 بكسل)
            # هذه المنطقة هي المساحة المخصصة لرسم الكتلة داخل الصندوق الجانبي
            target_grid_size_pixels = 4 * self.cell_size # 4 خلايا * 30 بكسل/خلية = 120 بكسل
            
            # حساب المسافة المتبقية في هذه المنطقة وتوزيعها بالتساوي على الجانبين
            center_offset_x = (target_grid_size_pixels - block_pixel_width) // 2
            center_offset_y = (target_grid_size_pixels - block_pixel_height) // 2
            
            # الإزاحات النهائية التي تُضاف إلى offset_x و offset_y القادمين من game.py
            # يجب طرح min_col * cell_size و min_row * cell_size لأن get_cell_positions()
            # تعطي المواقع النسبية للكتلة، ونريد أن نبدأ الرسم من 0،0 داخل المنطقة المحددة.
            draw_offset_x = offset_x + center_offset_x - (min_col * self.cell_size)
            draw_offset_y = offset_y + center_offset_y - (min_row * self.cell_size)
            
        else: # إذا لم نطلب التوسيط (كما هو الحال في الشبكة الرئيسية للعبة)
            draw_offset_x = offset_x
            draw_offset_y = offset_y

        for tile in tiles:
            # ارسم كل خلية من الكتلة بإزاحات التوسيط المحسوبة
            tile_rect = pygame.Rect(draw_offset_x + tile.column * self.cell_size,
                                    draw_offset_y + tile.row * self.cell_size,
                                    self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    def reset_position(self):
        self.row_offset = 0
        self.column_offset = 3 # Default spawn to center (column 3, can be adjusted)
