import os
import pygame, sys
from game import Game
from colors import Colors

# Initialize Pygame
pygame.init()
pygame.font.init()

# Fonts
title_font = pygame.font.Font(None, 40)
menu_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)
score_list_font = pygame.font.Font(None, 35)

# Render text surfaces
score_surface = title_font.render("Score", True, Colors.helwan_grey_light)
next_surface = title_font.render("Next Block", True, Colors.helwan_grey_light)
game_over_surface = title_font.render("SYSTEM HALTED", True, Colors.helwan_grey_light)
held_surface = title_font.render("Held Block", True, Colors.helwan_grey_light)

start_game_surface = menu_font.render("START GAME", True, Colors.helwan_green_accent)
instructions_surface = menu_font.render("INSTRUCTIONS", True, Colors.helwan_blue_medium)
high_scores_surface = menu_font.render("HIGH SCORES", True, Colors.helwan_orange_warm)
exit_game_surface = menu_font.render("EXIT", True, Colors.helwan_red_light)

game_title_surface = pygame.font.Font(None, 80).render("HELWAN BLOCKS", True, Colors.helwan_grey_light)

# --- تصحيح مسار الصورة ---
base_path = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_path, "Images", "helwan_logo.png")

try:
    helwan_logo_full = pygame.image.load(logo_path)
    helwan_logo_full = pygame.transform.scale(helwan_logo_full, (150, 150))
except pygame.error as e:
    print(f"Warning: Could not load helwan_logo.png - {e}")
    helwan_logo_full = None

try:
    window_icon = pygame.image.load(logo_path)
    pygame.display.set_icon(window_icon)
except pygame.error as e:
    print(f"Warning: Could not load window icon - {e}")

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
held_block_rect = pygame.Rect(320, 400, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Helwan Blocks")

clock = pygame.time.Clock()
game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())

game_state = "MENU"

def draw_menu():
    screen.fill(Colors.helwan_blue_dark)
    title_rect = game_title_surface.get_rect(center=(250, 110))
    screen.blit(game_title_surface, title_rect)

    if helwan_logo_full:
        logo_rect = helwan_logo_full.get_rect(center=(250, 240))
        screen.blit(helwan_logo_full, logo_rect)

    start_rect = start_game_surface.get_rect(center=(250, 370))
    instructions_rect = instructions_surface.get_rect(center=(250, 440))
    high_scores_rect = high_scores_surface.get_rect(center=(250, 510))
    exit_rect = exit_game_surface.get_rect(center=(250, 580))

    screen.blit(start_game_surface, start_rect)
    screen.blit(instructions_surface, instructions_rect)
    screen.blit(high_scores_surface, high_scores_rect)
    screen.blit(exit_game_surface, exit_rect)

    return {"start": start_rect, "instructions": instructions_rect, "high_scores": high_scores_rect, "exit": exit_rect}

def draw_instructions():
    screen.fill(Colors.helwan_blue_dark)
    instructions_title = menu_font.render("How To Play", True, Colors.helwan_grey_light)
    screen.blit(instructions_title, instructions_title.get_rect(center=(250, 50)))

    lines = [
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

    y = 150
    for line in lines:
        text = small_font.render(line, True, Colors.helwan_grey_light)
        screen.blit(text, text.get_rect(centerx=250, y=y))
        y += 40

    back_text = small_font.render("Press 'M' to return to Menu", True, Colors.helwan_orange_warm)
    screen.blit(back_text, back_text.get_rect(centerx=250, y=550))

def draw_highscores():
    screen.fill(Colors.helwan_blue_dark)
    title = menu_font.render("HIGH SCORES", True, Colors.helwan_grey_light)
    screen.blit(title, title.get_rect(center=(250, 50)))

    scores = game.highscores
    if not scores:
        text = small_font.render("No scores yet. Play to set one!", True, Colors.helwan_grey_light)
        screen.blit(text, text.get_rect(center=(250, 300)))
    else:
        y = 150
        for i, score in enumerate(scores):
            line = f"{i+1}. {score}"
            color = Colors.helwan_green_accent if i == 0 else Colors.helwan_grey_light
            text = score_list_font.render(line, True, color)
            screen.blit(text, text.get_rect(centerx=250, y=y))
            y += 40

    back_text = small_font.render("Press 'M' to return to Menu", True, Colors.helwan_orange_warm)
    screen.blit(back_text, back_text.get_rect(centerx=250, y=550))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "MENU":
                menu_rects = draw_menu()
                if menu_rects["start"].collidepoint(event.pos):
                    game_state = "PLAYING"
                    game.reset()
                    pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())
                elif menu_rects["instructions"].collidepoint(event.pos):
                    game_state = "INSTRUCTIONS"
                elif menu_rects["high_scores"].collidepoint(event.pos):
                    game_state = "HIGH_SCORES"
                elif menu_rects["exit"].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == "PLAYING":
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.game_over = False
                        game_state = "PLAYING"
                        game.reset()
                        pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())
                    elif event.key == pygame.K_m:
                        game_state = "MENU"
                else:
                    if event.key == pygame.K_LEFT: game.move_left()
                    if event.key == pygame.K_RIGHT: game.move_right()
                    if event.key == pygame.K_DOWN:
                        game.move_down()
                        game.update_score(0, 1)
                    if event.key == pygame.K_UP: game.rotate()
                    if event.key == pygame.K_SPACE:
                        game.hard_drop()
                        game.update_score(0, game.hard_drop_points)
                    if event.key == pygame.K_c: game.hold_block()
            elif event.key == pygame.K_m:
                game_state = "MENU"
            elif event.key == pygame.K_r and game_state == "GAME_OVER":
                game_state = "PLAYING"
                game.reset()
                pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())

        if event.type == GAME_UPDATE and game_state == "PLAYING" and not game.game_over:
            game.move_down()
            pygame.time.set_timer(GAME_UPDATE, game.get_drop_speed())

    if game_state == "MENU":
        draw_menu()
    elif game_state == "INSTRUCTIONS":
        draw_instructions()
    elif game_state == "HIGH_SCORES":
        draw_highscores()
    elif game_state in ["PLAYING", "GAME_OVER"]:
        screen.fill(Colors.dark_blue)

        score_value_surface = title_font.render(str(game.score), True, Colors.helwan_grey_light)
        screen.blit(score_surface, (365, 20))
        screen.blit(next_surface, (360, 180))
        screen.blit(held_surface, (360, 360))

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(center=score_rect.center))

        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, held_block_rect, 0, 10)

        game.draw(screen)

        if game.game_over:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            if helwan_logo_full:
                logo_rect = helwan_logo_full.get_rect(center=(250, 300))
                screen.blit(helwan_logo_full, logo_rect)

            rect = game_over_surface.get_rect(center=(250, 450))
            screen.blit(game_over_surface, rect)

            restart_text = small_font.render("Press 'R' to Restart", True, Colors.helwan_grey_light)
            menu_text = small_font.render("Press 'M' for Menu", True, Colors.helwan_grey_light)
            screen.blit(restart_text, restart_text.get_rect(centerx=250, y=500))
            screen.blit(menu_text, menu_text.get_rect(centerx=250, y=530))

    pygame.display.update()
    clock.tick(60)
