import pygame
import sys
import os # <--- إضافة مهمة: استيراد مكتبة os
from game import Game
from colors import Colors

# --- بداية التعديل: تحديد المسار الأساسي للمشروع ---
# ده بيجيب المسار المطلق للمجلد اللي فيه ملف main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# لو صورك ومجلداتك زي Sounds و Images موجودة مباشرة جنب main.py، يبقى كده تمام
assets_base_path = current_dir
# --- نهاية التعديل ---

pygame.init()
pygame.display.set_caption("Helwan Blocks")

# --- التعديل هنا: استخدام os.path.join لتحديد مسار الأيقونة والشعار ---
# حمل الأيقونة للنافذة
try:
    window_icon = pygame.image.load(os.path.join(assets_base_path, "Images", "helwan_logo.png"))
    pygame.display.set_icon(window_icon)
except pygame.error as e:
    print(f"Warning: Could not load window icon - {e}")
    # استخدم أيقونة بديلة أو لا تضع أيقونة إذا فشل التحميل

# الألوان
dark_grey = (44, 44, 44)
green = (173, 204, 114)
light_blue = (59, 85, 162) # لون جديد للواجهة الخلفية

screen_width = 500
screen_height = 620
screen = pygame.display.set_mode((screen_width, screen_height))

game = Game() # إنشاء كائن اللعبة

# الأيقونة الرئيسية للخلفية
# --- التعديل هنا: استخدام os.path.join لتحديد مسار الشعار الرئيسي ---
try:
    helwan_logo_full = pygame.image.load(os.path.join(assets_base_path, "Images", "helwan_logo.png"))
    # تصغير حجم الشعار ليتناسب مع الواجهة
    helwan_logo_full = pygame.transform.scale(helwan_logo_full, (200, 200)) # مثال لحجم مناسب
except pygame.error as e:
    print(f"Warning: Could not load full logo - {e}")
    helwan_logo_full = None # لا تضع الشعار إذا فشل التحميل

# الخطوط
score_font = pygame.font.Font(None, 36) # خط للنقاط
title_font = pygame.font.Font(None, 48) # خط للعناوين
level_font = pygame.font.Font(None, 28) # خط للمستويات
game_over_font = pygame.font.Font(None, 60) # خط لـ Game Over
# خط مخصص لقائمة High Scores (يمكنك تغيير الفونت لخط نظام أو خط مخصص)
highscore_font = pygame.font.Font(None, 24)

# حدث تدوير الكتلة تلقائياً
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) # سرعة السقوط الأولية

# --- Helwan Linux Customization: Game Loop State ---
# إضافة حالة للعبة للتحكم في الواجهات (menu, playing, game_over)
game_state = "playing" # ابدأ اللعبة مباشرة في وضع اللعب

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.game_over == True: # لو اللعبة انتهت
                if event.key == pygame.K_r: # مفتاح R لإعادة التشغيل
                    game.reset()
                    game_state = "playing" # الرجوع لوضع اللعب
                elif event.key == pygame.K_q: # مفتاح Q للخروج من اللعبة
                    pygame.quit()
                    sys.exit()
            elif game_state == "playing": # لو اللعبة شغالة
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1) # نقطة إضافية لكل سقوط يدوي
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE: # مفتاح Space لـ Hard Drop
                    game.hard_drop()
                    # نقاط السقوط القاسي يتم إضافتها في دالة lock_block()
                elif event.key == pygame.K_c: # مفتاح C لـ Hold Block
                    game.hold_block()

        if event.type == GAME_UPDATE and game.game_over == False and game_state == "playing":
            game.move_down()
            # تحديث سرعة السقوط بناءً على المستوى الجديد
            pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())


    # رسم الشاشة
    screen.fill(light_blue) # خلفية زرقاء فاتحة للنافذة

    if game.game_over == True:
        # شاشة نهاية اللعبة
        game_over_text = game_over_font.render("GAME OVER", True, Colors.red)
        score_final_text = score_font.render(f"Final Score: {game.score}", True, Colors.white)
        restart_text = score_font.render("Press 'R' to Restart", True, Colors.white)
        quit_text = score_font.render("Press 'Q' to Quit", True, Colors.white)

        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 80))
        score_final_rect = score_final_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
        quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))


        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_final_text, score_final_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        # عرض قائمة أعلى النقاط
        highscore_title = score_font.render("TOP SCORES", True, Colors.yellow)
        screen.blit(highscore_title, (screen_width // 2 - highscore_title.get_width() // 2, screen_height // 2 + 120))
        
        y_offset = 150
        for i, score_val in enumerate(game.highscores):
            score_line = highscore_font.render(f"{i+1}. {score_val}", True, Colors.white)
            screen.blit(score_line, (screen_width // 2 - score_line.get_width() // 2, screen_height // 2 + y_offset + (i * 25)))
        

    elif game_state == "playing": # لو اللعبة شغالة
        # رسم خلفية اللعبة
        game.draw(screen)

        # رسم اللوحة الجانبية (Score, Next Block, Held Block)
        # لوحة Score
        score_board_rect = pygame.Rect(320, 50, 170, 70) # تغيير مكان لوحة Score
        pygame.draw.rect(screen, Colors.light_blue_helwan, score_board_rect, 0, 10)
        score_title_text = score_font.render("Score", True, Colors.white)
        score_value_text = score_font.render(str(game.score), True, Colors.white)
        screen.blit(score_title_text, score_board_rect.centerx - score_title_text.get_width() / 2, score_board_rect.y + 10)
        screen.blit(score_value_text, score_board_rect.centerx - score_value_text.get_width() / 2, score_board_rect.y + 35)

        # لوحة Next Block
        next_block_board_rect = pygame.Rect(320, 150, 170, 120) # تغيير مكان لوحة Next Block
        pygame.draw.rect(screen, Colors.light_blue_helwan, next_block_board_rect, 0, 10)
        next_title_text = score_font.render("Next", True, Colors.white)
        screen.blit(next_title_text, next_block_board_rect.centerx - next_title_text.get_width() / 2, next_block_board_rect.y + 10)

        # لوحة Held Block
        held_block_board_rect = pygame.Rect(320, 330, 170, 120) # تغيير مكان لوحة Held Block
        pygame.draw.rect(screen, Colors.light_blue_helwan, held_block_board_rect, 0, 10)
        held_title_text = score_font.render("Hold", True, Colors.white)
        screen.blit(held_title_text, held_block_board_rect.centerx - held_title_text.get_width() / 2, held_block_board_rect.y + 10)

        # لوحة Level
        level_board_rect = pygame.Rect(320, 510, 170, 70) # تغيير مكان لوحة Level
        pygame.draw.rect(screen, Colors.light_blue_helwan, level_board_rect, 0, 10)
        level_title_text = level_font.render("Level", True, Colors.white)
        level_value_text = level_font.render(str(game.level), True, Colors.white)
        screen.blit(level_title_text, level_board_rect.centerx - level_title_text.get_width() / 2, level_board_rect.y + 10)
        screen.blit(level_value_text, level_board_rect.centerx - level_value_text.get_width() / 2, level_board_rect.y + 35)

        # رسم شعار Helwan Linux في الجانب
        if helwan_logo_full:
            # وضع الشعار في منتصف العمود الأيمن تحت الـ held block
            logo_x = 320 + (170 - helwan_logo_full.get_width()) // 2
            logo_y = 450 + (620 - 450 - helwan_logo_full.get_height()) // 2 # لأسفل الشاشة
            screen.blit(helwan_logo_full, (logo_x, logo_y))


    pygame.display.update()
