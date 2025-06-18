import pygame
import sys
import os
from game import Game
from colors import Colors

# --- بداية التعديل: تحديد المسار الأساسي للمشروع ---
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_base_path = current_dir
# --- نهاية التعديل ---

pygame.init()
pygame.display.set_caption("Helwan Blocks")

# استخدام os.path.join لتحديد مسار الأيقونة والشعار
try:
    window_icon = pygame.image.load(os.path.join(assets_base_path, "Images", "helwan_logo.png"))
    pygame.display.set_icon(window_icon)
except pygame.error as e:
    print(f"Warning: Could not load window icon - {e}")

# الألوان
dark_grey = (44, 44, 44)
green = (173, 204, 114)
light_blue = (59, 85, 162) # لون جديد للواجهة الخلفية

screen_width = 500
screen_height = 620
screen = pygame.display.set_mode((screen_width, screen_height))

game = Game()

# الأيقونة الرئيسية للخلفية
try:
    helwan_logo_full = pygame.image.load(os.path.join(assets_base_path, "Images", "helwan_logo.png"))
    # تعديل هنا: تصغير حجم الشعار لـ 150x150 ليتناسب بشكل أفضل
    helwan_logo_full = pygame.transform.scale(helwan_logo_full, (150, 150))
except pygame.error as e:
    print(f"Warning: Could not load full logo - {e}")
    helwan_logo_full = None

# الخطوط
score_font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)
level_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 60)
highscore_font = pygame.font.Font(None, 24)
# خط جديد لشاشة البداية (ممكن نستخدم score_font أو menu_font لو محتاج حجم مختلف)
menu_font = pygame.font.Font(None, 40) # خط لأزرار القائمة

# حدث تدوير الكتلة تلقائياً
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())

# إضافة حالة جديدة لـ "إرشادات"
game_state = "start_screen" # اللعبة هتبدأ بشاشة البداية

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == "start_screen":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN: # Space or Enter to Play
                    game_state = "playing"
                    game.reset() # إعادة ضبط اللعبة لما تبدأ من شاشة البداية
                    pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) # إعادة ضبط التايمر
                elif event.key == pygame.K_i: # 'I' for Instructions
                    game_state = "instructions_screen"
                elif event.key == pygame.K_q: # Q to Quit
                    pygame.quit()
                    sys.exit()
            elif game_state == "instructions_screen":
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE: # Esc or Backspace to go back
                    game_state = "start_screen"
            elif game.game_over == True:
                if event.key == pygame.K_r:
                    game.reset()
                    game_state = "playing"
                    pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) # إعادة ضبط التايمر
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif game_state == "playing":
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_c:
                    game.hold_block()

        if event.type == GAME_UPDATE and game.game_over == False and game_state == "playing":
            game.move_down()
            pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())

    screen.fill(light_blue)

    # --- منطق شاشة البداية ---
    if game_state == "start_screen":
        # رسم الشعار في المنتصف العلوي
        if helwan_logo_full:
            logo_x = screen_width // 2 - helwan_logo_full.get_width() // 2
            logo_y = screen_height // 2 - helwan_logo_full.get_height() // 2 - 100 # أعلى الشاشة قليلا
            screen.blit(helwan_logo_full, (logo_x, logo_y))

        # عنوان اللعبة (اختياري لو الشعار بيكفي)
        game_title_text = title_font.render("Helwan Blocks", True, Colors.white)
        game_title_rect = game_title_text.get_rect(center=(screen_width // 2, logo_y + helwan_logo_full.get_height() + 10))
        screen.blit(game_title_text, game_title_rect)


        # زر "ابدأ اللعب"
        play_text = menu_font.render("Press SPACE to Play", True, Colors.white)
        play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(play_text, play_rect)

        # زر "إرشادات"
        instructions_text = menu_font.render("Press I for Instructions", True, Colors.white)
        instructions_rect = instructions_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(instructions_text, instructions_rect)

        # أعلى سكور
        high_score_title = score_font.render("High Score", True, Colors.yellow)
        high_score_value = score_font.render(str(game.highscores[0]) if game.highscores else "0", True, Colors.white)
        
        high_score_title_rect = high_score_title.get_rect(center=(screen_width // 2, screen_height // 2 + 180))
        high_score_value_rect = high_score_value.get_rect(center=(screen_width // 2, screen_height // 2 + 210))

        screen.blit(high_score_title, high_score_title_rect)
        screen.blit(high_score_value, high_score_value_rect)

        # زر Quit
        quit_text_menu = score_font.render("Press Q to Quit", True, Colors.white)
        quit_rect_menu = quit_text_menu.get_rect(center=(screen_width // 2, screen_height - 30)) # تحت خالص
        screen.blit(quit_text_menu, quit_rect_menu)

    # --- منطق شاشة الإرشادات ---
    elif game_state == "instructions_screen":
        instructions_title = title_font.render("Instructions", True, Colors.white)
        instructions_title_rect = instructions_title.get_rect(center=(screen_width // 2, 50))
        screen.blit(instructions_title, instructions_title_rect)

        # نص الإرشادات (ممكن تزود التفاصيل هنا)
        instruction_lines = [
            "Use Left/Right Arrows to Move Block",
            "Use Down Arrow for Soft Drop",
            "Use Up Arrow to Rotate Block",
            "Use SPACE for Hard Drop",
            "Use C to Hold/Swap Block",
            "Clear full rows to score points",
            "Get a Game Over when blocks stack to the top",
            "Press ESC or BACKSPACE to go back"
        ]
        
        y_offset_inst = 120
        for line in instruction_lines:
            line_text = score_font.render(line, True, Colors.white)
            line_rect = line_text.get_rect(center=(screen_width // 2, y_offset_inst))
            screen.blit(line_text, line_rect)
            y_offset_inst += 40

    elif game.game_over == True:
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

        highscore_title = score_font.render("TOP SCORES", True, Colors.yellow)
        screen.blit(highscore_title, (screen_width // 2 - highscore_title.get_width() / 2, screen_height // 2 + 120))
        
        y_offset = 150
        for i, score_val in enumerate(game.highscores):
            score_line = highscore_font.render(f"{i+1}. {score_val}", True, Colors.white)
            screen.blit(score_line, (screen_width // 2 - score_line.get_width() / 2, screen_height // 2 + y_offset + (i * 25)))
        

    elif game_state == "playing":
        
        game.draw(screen) # دي بترسم الشبكة والقطع

        score_board_rect = pygame.Rect(320, 50, 170, 70)
        pygame.draw.rect(screen, Colors.light_blue_helwan, score_board_rect, 0, 10)
        score_title_text = score_font.render("Score", True, Colors.white)
        score_value_text = score_font.render(str(game.score), True, Colors.white)
        screen.blit(score_title_text, (score_board_rect.centerx - score_title_text.get_width() / 2, score_board_rect.y + 10))
        screen.blit(score_value_text, (score_board_rect.centerx - score_value_text.get_width() / 2, score_board_rect.y + 35))

        next_block_board_rect = pygame.Rect(320, 150, 170, 120)
        pygame.draw.rect(screen, Colors.light_blue_helwan, next_block_board_rect, 0, 10)
        next_title_text = score_font.render("Next", True, Colors.white)
        screen.blit(next_title_text, (next_block_board_rect.centerx - next_title_text.get_width() / 2, next_block_board_rect.y + 10))

        held_block_board_rect = pygame.Rect(320, 330, 170, 120)
        pygame.draw.rect(screen, Colors.light_blue_helwan, held_block_board_rect, 0, 10)
        held_title_text = score_font.render("Hold", True, Colors.white)
        screen.blit(held_title_text, (held_block_board_rect.centerx - held_title_text.get_width() / 2, held_block_board_rect.y + 10))

        level_board_rect = pygame.Rect(320, 510, 170, 70)
        pygame.draw.rect(screen, Colors.light_blue_helwan, level_board_rect, 0, 10)
        level_title_text = level_font.render("Level", True, Colors.white)
        level_value_text = level_font.render(str(game.level), True, Colors.white)
        screen.blit(level_title_text, (level_board_rect.centerx - level_title_text.get_width() / 2, level_board_rect.y + 10))
        screen.blit(level_value_text, (level_board_rect.centerx - level_value_text.get_width() / 2, level_board_rect.y + 35))
        
        # وضع الشعار في مكان مختلف لتجنب التداخل
        if helwan_logo_full:
            logo_x = 320 + (170 - helwan_logo_full.get_width()) // 2
            logo_y = level_board_rect.y + level_board_rect.height + 10 # 10 بكسل تحت صندوق الليفل
            screen.blit(helwan_logo_full, (logo_x, logo_y))


    pygame.display.update()
