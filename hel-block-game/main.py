import os
import pygame,sys
from game import Game
from colors import Colors

# Initialize Pygame
pygame.init()
pygame.font.init() # Ensure font module is initialized

# --- Helwan Linux Customization ---
title_font = pygame.font.Font(None, 40)
menu_font = pygame.font.Font(None, 50) # خط أكبر لشاشة القائمة
small_font = pygame.font.Font(None, 30) # خط أصغر للتعليمات
score_list_font = pygame.font.Font(None, 35) # خط لعرض قائمة النقاط

# Render text surfaces (updated to use Helwan colors)
score_surface = title_font.render("Score", True, Colors.helwan_grey_light)
next_surface = title_font.render("Next Block", True, Colors.helwan_grey_light)
game_over_surface = title_font.render("SYSTEM HALTED", True, Colors.helwan_grey_light)
held_surface = title_font.render("Held Block", True, Colors.helwan_grey_light) # نص "Held Block"

# Menu Text Surfaces (Updated to include High Scores)
start_game_surface = menu_font.render("START GAME", True, Colors.helwan_green_accent)
instructions_surface = menu_font.render("INSTRUCTIONS", True, Colors.helwan_blue_medium)
high_scores_surface = menu_font.render("HIGH SCORES", True, Colors.helwan_orange_warm) # إضافة جديدة
exit_game_surface = menu_font.render("EXIT", True, Colors.helwan_red_light) # لون جديد للخروج

# Game Title on Menu Screen
game_title_surface = pygame.font.Font(None, 80).render("HELWAN BLOCKS", True, Colors.helwan_grey_light)

# Load Helwan Linux Logo
try:
    helwan_logo_full = pygame.image.load("Images/helwan_logo.png")
    helwan_logo_full = pygame.transform.scale(helwan_logo_full, (150, 150)) # For menu screen
except pygame.error as e:
    print(f"Warning: Could not load helwan_logo.png - {e}")
    helwan_logo_full = None

# --- التعديل هنا: تصحيح المسار لاستخدام Images/helwan_logo.png ---
try:
    # Pygame يمكنه استخدام PNGs كأيقونات للنوافذ على Linux و Windows
    window_icon = pygame.image.load("Images/helwan_logo.png") 
    pygame.display.set_icon(window_icon)
except pygame.error as e:
    print(f"Warning: Could not load window icon (Images/helwan_logo.png) - {e}")
    # إذا استمرت المشكلة، يمكنك طباعة مسار العمل الحالي للمزيد من Debugging
    # import os
    # print(f"Current working directory: {os.getcwd()}")


# Rectangles for UI elements
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
# --- Helwan Linux Customization: Held Block Display Area ---
held_block_rect = pygame.Rect(320, 400, 170, 180) # مستطيل جديد لعرض القطعة المحفوظة

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Helwan Blocks")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) # Initial speed

# --- إضافة جديدة: حالة اللعبة ---
game_state = "MENU" # يمكن أن تكون "MENU", "PLAYING", "INSTRUCTIONS", "HIGH_SCORES", "GAME_OVER"

def draw_menu():
    screen.fill(Colors.helwan_blue_dark) # خلفية قائمة
    
    # Draw Game Title
    title_rect = game_title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))
    screen.blit(game_title_surface, title_rect)

    # Draw Helwan Logo on Menu
    if helwan_logo_full:
        logo_rect = helwan_logo_full.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 80))
        screen.blit(helwan_logo_full, logo_rect)

    # Draw Menu Options
    start_rect = start_game_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    instructions_rect = instructions_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 120))
    high_scores_rect = high_scores_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 190)) # إضافة جديدة
    exit_rect = exit_game_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 260)) # تعديل موضع زر الخروج

    screen.blit(start_game_surface, start_rect)
    screen.blit(instructions_surface, instructions_rect)
    screen.blit(high_scores_surface, high_scores_rect) # رسم زر أعلى النقاط
    screen.blit(exit_game_surface, exit_rect)

    # Return rects for click detection
    return {"start": start_rect, "instructions": instructions_rect, "high_scores": high_scores_rect, "exit": exit_rect} # إرجاع Rects الجديدة

def draw_instructions():
    screen.fill(Colors.helwan_blue_dark)
    instructions_title = menu_font.render("How To Play", True, Colors.helwan_grey_light)
    screen.blit(instructions_title, instructions_title.get_rect(center=(screen.get_width() // 2, 50)))

    instruction_lines = [
        "Left/Right Arrow: Move Block",
        "Down Arrow: Soft Drop",
        "Up Arrow: Rotate Block",
        "Spacebar: Hard Drop",
        "C Key: Hold/Swap Block", 
        "Clear full rows to score points!",
        "Clear multiple rows for more points!",
        "Clear rows consecutively for Combo Bonus!",
        "Level increases as you clear lines!",
        "Press 'M' to return to Menu"
    ]

    y_offset = 150
    for line in instruction_lines:
        line_surface = small_font.render(line, True, Colors.helwan_grey_light)
        screen.blit(line_surface, line_surface.get_rect(centerx=screen.get_width() // 2, y=y_offset))
        y_offset += 40 # Spacing between lines

    back_to_menu_surface = small_font.render("Press 'M' to return to Menu", True, Colors.helwan_orange_warm)
    screen.blit(back_to_menu_surface, back_to_menu_surface.get_rect(centerx=screen.get_width() // 2, y=550))

# --- إضافة جديدة: دالة لرسم شاشة أعلى النقاط ---
def draw_highscores():
    screen.fill(Colors.helwan_blue_dark)
    highscore_title = menu_font.render("HIGH SCORES", True, Colors.helwan_grey_light)
    screen.blit(highscore_title, highscore_title.get_rect(center=(screen.get_width() // 2, 50)))

    scores = game.highscores # الحصول على النقاط من كائن اللعبة
    if not scores:
        no_scores_text = small_font.render("No scores yet. Play to set one!", True, Colors.helwan_grey_light)
        screen.blit(no_scores_text, no_scores_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))
    else:
        y_offset = 150
        for i, score in enumerate(scores):
            score_text = f"{i+1}. {score}"
            score_surface_rendered = score_list_font.render(score_text, True, Colors.helwan_green_accent if i == 0 else Colors.helwan_grey_light)
            screen.blit(score_surface_rendered, score_surface_rendered.get_rect(centerx=screen.get_width() // 2, y=y_offset))
            y_offset += 40

    back_to_menu_surface = small_font.render("Press 'M' to return to Menu", True, Colors.helwan_orange_warm)
    screen.blit(back_to_menu_surface, back_to_menu_surface.get_rect(centerx=screen.get_width() // 2, y=550))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button
            if game_state == "MENU":
                menu_rects = draw_menu() # Get rects to check clicks
                if menu_rects["start"].collidepoint(event.pos):
                    game_state = "PLAYING"
                    game.reset() # Reset game if starting from menu
                    pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) # Reset timer
                elif menu_rects["instructions"].collidepoint(event.pos):
                    game_state = "INSTRUCTIONS"
                elif menu_rects["high_scores"].collidepoint(event.pos): # إضافة جديدة
                    game_state = "HIGH_SCORES"
                elif menu_rects["exit"].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == "PLAYING":
                if game.game_over == True:
                    if event.key == pygame.K_r: # Changed reset key to 'R'
                        game.game_over = False
                        game_state = "PLAYING"
                        game.reset()
                        pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())
                    elif event.key == pygame.K_m: # 'M' to return to menu from Game Over
                        game_state = "MENU"
                else: # Only process game controls if not game over
                    if event.key == pygame.K_LEFT:
                        game.move_left()
                    if event.key == pygame.K_RIGHT:
                        game.move_right()
                    if event.key == pygame.K_DOWN:
                        game.move_down()
                        game.update_score(0, 1)
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_SPACE:
                        game.hard_drop()
                        game.update_score(0, game.hard_drop_points)
                    if event.key == pygame.K_c: # Hotkey for Hold Piece
                        game.hold_block()

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r: # 'R' to restart after Game Over
                    game.game_over = False
                    game_state = "PLAYING"
                    game.reset()
                    pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())
                elif event.key == pygame.K_m: # 'M' to return to menu from Game Over
                    game_state = "MENU"
            elif game_state == "INSTRUCTIONS":
                if event.key == pygame.K_m: # 'M' to return to menu from Instructions
                    game_state = "MENU"
            elif game_state == "HIGH_SCORES": # إضافة جديدة: العودة من شاشة أعلى النقاط
                if event.key == pygame.K_m:
                    game_state = "MENU"


        if event.type == GAME_UPDATE and game_state == "PLAYING" and game.game_over == False:
            game.move_down()
            pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed()) # Update speed

    # --- Drawing Logic based on Game State ---
    if game_state == "MENU":
        draw_menu()
    elif game_state == "INSTRUCTIONS":
        draw_instructions()
    elif game_state == "HIGH_SCORES": # إضافة جديدة
        draw_highscores()
    elif game_state == "PLAYING" or game_state == "GAME_OVER":
        score_value_surface = title_font.render(str(game.score), True, Colors.helwan_grey_light)
        screen.fill(Colors.dark_blue)

        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (360, 180, 50, 50))
        screen.blit(held_surface, (360, 360, 50, 50)) # نص "Held Block"

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
            centery = score_rect.centery))

        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, held_block_rect, 0, 10) # مستطيل القطعة المحفوظة

        game.draw(screen) # Draw grid, current block, ghost block, next block, and held block

        if game.game_over == True:
            # Add a semi-transparent overlay
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Black with 150/255 transparency
            screen.blit(overlay, (0, 0))

            if helwan_logo_full: # Use the full logo for game over
                logo_rect = helwan_logo_full.get_rect(centerx = screen.get_width() / 2, centery = 300)
                screen.blit(helwan_logo_full, logo_rect)
            game_over_rect = game_over_surface.get_rect(centerx = screen.get_width() / 2, centery = 450)
            screen.blit(game_over_surface, game_over_rect)
            
            # Display Restart/Menu instructions
            restart_text = small_font.render("Press 'R' to Restart", True, Colors.helwan_grey_light)
            menu_text = small_font.render("Press 'M' for Menu", True, Colors.helwan_grey_light)
            screen.blit(restart_text, restart_text.get_rect(centerx=screen.get_width()/2, y=500))
            screen.blit(menu_text, menu_text.get_rect(centerx=screen.get_width()/2, y=530))


    pygame.display.update()
    clock.tick(60)
