class Colors:
    # الألوان الأساسية
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    orange = (255, 165, 0)
    purple = (128, 0, 128)
    cyan = (0, 255, 255)
    grey = (100, 100, 100) # لون رمادي عام
    pink = (255, 192, 203)

    # ألوان Helwan Linux المخصصة
    helwan_dark_blue = (36, 52, 90)
    light_blue_helwan = (59, 85, 162) # <--- تم توحيد الاسم هنا ليتطابق مع main.py
    helwan_grey_light = (180, 180, 180) # لون رمادي فاتح لـ Ghost Piece

    # تعريف الألوان للقطع
    I = (0, 255, 255) # Cyan
    J = (0, 0, 255)   # Blue
    L = (255, 165, 0) # Orange
    O = (255, 255, 0) # Yellow
    S = (0, 255, 0)   # Green
    T = (128, 0, 128) # Purple
    Z = (255, 0, 0)   # Red

    # قائمة الألوان المستخدمة لسهولة الوصول (بما في ذلك الألوان المخصصة لـ Helwan)
    block_colors = [
        helwan_dark_blue, # اللون 1 (مثال)
        light_blue_helwan, # اللون 2 (مثال)
        helwan_grey_light, # اللون 3 (مثال)
        I, J, L, O, S, T, Z
    ]

    # قائمة بألوان القطع بالترتيب (أرقام 1-7)
    # index 0 is not used, actual colors start from index 1
    # this aligns with block.id values (1 to 7)
    get_cell_colors = [
        (0,0,0), # Placeholder for index 0, not used
        I, J, L, O, S, T, Z
    ]
