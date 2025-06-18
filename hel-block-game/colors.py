class Colors:
    dark_grey = (44, 44, 44)
    green = (173, 204, 114)
    light_blue = (59, 85, 162) 
    white = (255, 255, 255)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    purple = (150, 0, 150) 

    block_colors = {
        0: (0, 0, 0), # لون للخلية الفارغة في الشبكة (أسود) - مهم يكون موجود
        1: (20, 160, 240), # I-block (Light Blue)
        2: (255, 165, 0),  # J-block (Orange)
        3: (48, 211, 56),  # L-block (Green)
        4: (240, 240, 0),  # O-block (Yellow)
        5: (100, 50, 100), # S-block (Purple)
        6: (180, 0, 255),  # T-block (Magenta)
        7: (220, 38, 18),  # Z-block (Red)
    }
    
    helwan_blue = (0, 0, 128)
    helwan_gold = (218, 165, 32)
    helwan_grey_light = (180, 180, 180) 
    helwan_grey_dark = (80, 80, 80) 
    helwan_light_blue_bg = (100, 100, 200)
    helwan_light_blue = (90, 90, 220)
