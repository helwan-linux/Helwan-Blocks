class Colors:
    # --- Helwan Linux Customization: New Color Palette ---
    # These colors aim to give a clean, modern, and distinct feel,
    # reminiscent of a Linux distribution's UI.

    # Primary Helwan-inspired colors
    helwan_blue_dark = (30, 70, 100)    # Deeper blue, possibly for backgrounds
    helwan_blue_medium = (45, 90, 130)  # Mid-range blue, for panels/elements
    helwan_green_accent = (50, 200, 120) # A vibrant green for accents or active elements
    helwan_orange_warm = (240, 150, 70) # A warm orange for highlights or warnings
    helwan_grey_light = (200, 200, 200) # Light grey for text or subtle outlines
    helwan_grey_dark = (60, 60, 60)     # Dark grey for text or shadows
    helwan_red_light = (255, 90, 90)    # Light red for exit/warnings

    # Tetris block specific colors (updated to fit Helwan theme)
    # Mapping block IDs to these new colors for a cohesive look
    block_color_1 = (25, 130, 170)  # LBlock (Cyan-ish)
    block_color_2 = (180, 70, 10)   # JBlock (Red-Orange)
    block_color_3 = (200, 20, 20)   # IBlock (Vibrant Red)
    block_color_4 = (240, 200, 0)   # OBlock (Bright Yellow)
    block_color_5 = (60, 180, 60)   # SBlock (Fresh Green)
    block_color_6 = (150, 50, 200)  # TBlock (Deep Purple)
    block_color_7 = (200, 80, 20)   # ZBlock (Darker Orange)


    # Core UI colors (used in main.py for background and score/next panels)
    # Using the new Helwan-inspired palette
    white = helwan_grey_light      # White text changed to light grey for softer look
    dark_blue = helwan_blue_dark   # Main background
    light_blue = helwan_blue_medium # Panels background

    @classmethod
    def get_cell_colors(cls):
        # The list now uses the new block-specific colors.
        # The first element (index 0) corresponds to the 'dark_grey'
        # which is usually the empty grid color, and it's not used by blocks.
        return [
            cls.helwan_grey_dark, # This could be the grid lines/empty cell color
            cls.block_color_1, # ID 1: LBlock
            cls.block_color_2, # ID 2: JBlock
            cls.block_color_3, # ID 3: IBlock
            cls.block_color_4, # ID 4: OBlock
            cls.block_color_5, # ID 5: SBlock
            cls.block_color_6, # ID 6: TBlock
            cls.block_color_7  # ID 7: ZBlock
        ]
