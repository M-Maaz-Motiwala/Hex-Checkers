# main.py

import pygame
import sys
from settings import *
from tilemap import TILE_POSITIONS, INITIAL_PIECES
from game import Game

def display_winner(screen, winner):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont("arial", 64, bold=True)
    sub_font = pygame.font.SysFont("arial", 30)

    text = font.render(f"{winner.capitalize()} Wins!", True, (255, 215, 0))
    sub_text = sub_font.render("Click anywhere to return to the menu...", True, (220, 220, 220))

    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

    pygame.draw.rect(screen, (60, 60, 60), text_rect.inflate(40, 30), border_radius=10)
    screen.blit(text, text_rect)
    screen.blit(sub_text, sub_rect)

    pygame.display.update()
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

def draw_menu(screen):
    pygame.font.init()
    button_font = pygame.font.SysFont("arial", 36, bold=True)
    title_font = pygame.font.SysFont("verdana", 72, bold=True)
    shadow_color = (50, 50, 50)

    options = ["Player vs Player", "Player vs CPU (Easy)", "Player vs CPU (Hard)"]
    selected_index = 0

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((30, 30, 60))  # Dark blue tone

    while True:
        screen.blit(background, (0, 0))

        # Title with shadow
        title_text = title_font.render("Hexagon Checkers", True, (255, 255, 255))
        shadow_text = title_font.render("Hexagon Checkers", True, shadow_color)
        screen.blit(shadow_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 4, 154))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for idx, option in enumerate(options):
            is_hovered = False
            text = button_font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + idx * 80))
            button_rect = text_rect.inflate(40, 20)

            if button_rect.collidepoint(mouse_x, mouse_y):
                is_hovered = True
                selected_index = idx

            color = (70, 130, 180) if is_hovered else (50, 50, 50)
            pygame.draw.rect(screen, color, button_rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=12)
            screen.blit(text, text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    return ['pvp', 'pvcpu_easy', 'pvcpu_hard'][selected_index]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, option in enumerate(options):
                    text = button_font.render(option, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + idx * 80))
                    button_rect = text_rect.inflate(40, 20)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        return ['pvp', 'pvcpu_easy', 'pvcpu_hard'][idx]

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hexagon Checkers")

    board_img = pygame.image.load(BOARD_IMAGE_PATH)
    red_piece_img = pygame.transform.scale(pygame.image.load(RED_PIECE_IMAGE_PATH), (60, 60))
    blue_piece_img = pygame.transform.scale(pygame.image.load(BLUE_PIECE_IMAGE_PATH), (60, 60))
    red_king_img = pygame.transform.scale(pygame.image.load(RED_PIECE_KING_IMAGE_PATH), (60, 60))
    blue_king_img = pygame.transform.scale(pygame.image.load(BLUE_PIECE_KING_IMAGE_PATH), (60, 60))

    clock = pygame.time.Clock()

    while True:
        mode = draw_menu(screen)
        game = Game(INITIAL_PIECES, mode=mode)
        running = True

        while running:
            clock.tick(FPS)
            screen.fill((30, 30, 60))  # Clean, dark background

            # Draw the board
            screen.blit(board_img, (0, BOARD_Y))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    clicked_tile = None

                    for tile, (tx, ty) in TILE_POSITIONS.items():
                        if (mx - tx) ** 2 + (my - ty) ** 2 <= 30 ** 2:
                            clicked_tile = tile
                            break

                    if clicked_tile:
                        if game.tile_occupancy[clicked_tile]:
                            game.select_piece(clicked_tile)
                        else:
                            if game.selected_piece:
                                moved = game.move_selected_piece(clicked_tile)
                                if moved:
                                    winner = game.check_game_over()
                                    if winner or Game.AI:
                                        display_winner(screen, winner or Game.AI)
                                        Game.AI = None
                                        running = False

            for piece in game.pieces:
                is_selected = (piece == game.selected_piece)
                piece.draw(screen, red_piece_img, blue_piece_img, red_king_img, blue_king_img, is_selected)

            for tile in game.valid_moves:
                if tile != 'none':
                    x, y = TILE_POSITIONS[tile]
                    pygame.draw.circle(screen, (255, 255, 0), (x, y), 12)
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), 12, 2)

            pygame.display.flip()


if __name__ == "__main__":
    main()
