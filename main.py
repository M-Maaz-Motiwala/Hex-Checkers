# main.py

import pygame
import sys
from settings import *
from tilemap import TILE_POSITIONS, INITIAL_PIECES
from game import Game


def display_winner(screen, winner):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont("arial", 64, bold=True)
    sub_font = pygame.font.SysFont("arial", 32)

    text = font.render(f"{winner.capitalize()} Wins!", True, (255, 215, 0))
    sub_text = sub_font.render("Press any key to return to the main menu...", True, (200, 200, 200))

    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

    screen.blit(text, text_rect)
    screen.blit(sub_text, sub_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def draw_menu(screen):
    pygame.font.init()
    button_font = pygame.font.SysFont("arial", 36)
    title_font = pygame.font.SysFont("arial", 64)

    options = ["Player vs Player", "Player vs CPU (Easy)", "Player vs CPU (Hard)"]
    selected_index = 0

    while True:
        screen.fill((0, 0, 0))
        title_text = title_font.render("Hexagon Checkers", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for idx, option in enumerate(options):
            color = (255, 255, 0) if idx == selected_index else (255, 255, 255)
            text = button_font.render(f"{idx + 1}. {option}", True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + idx * 70))

            # Highlight background
            if idx == selected_index:
                pygame.draw.rect(screen, (100, 100, 100), text_rect.inflate(20, 10))

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
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return ['pvp', 'pvcpu_easy', 'pvcpu_hard'][selected_index]
                elif event.key == pygame.K_1:
                    return 'pvp'
                elif event.key == pygame.K_2:
                    return 'pvcpu_easy'
                elif event.key == pygame.K_3:
                    return 'pvcpu_hard'


            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, option in enumerate(options):
                    text = button_font.render(f"{idx + 1}. {option}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + idx * 70))
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        return ['pvp', 'pvcpu_easy', 'pvcpu_hard'][idx]


            elif event.type == pygame.MOUSEMOTION:
                for idx in range(len(options)):
                    text = button_font.render(f"{idx + 1}. {options[idx]}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + idx * 70))
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        selected_index = idx

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hexagon Checkers")

    board_img = pygame.image.load(BOARD_IMAGE_PATH)

    # board_img = pygame.transform.scale(board_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load pieces
    red_piece_img = pygame.transform.scale(pygame.image.load(RED_PIECE_IMAGE_PATH), (60, 60))
    blue_piece_img = pygame.transform.scale(pygame.image.load(BLUE_PIECE_IMAGE_PATH), (60, 60))
    red_king_img = pygame.transform.scale(pygame.image.load(RED_PIECE_KING_IMAGE_PATH), (60, 60))
    blue_king_img = pygame.transform.scale(pygame.image.load(BLUE_PIECE_KING_IMAGE_PATH), (60, 60))

    clock = pygame.time.Clock()

    while True:  # Loop to restart game after win
        mode = draw_menu(screen)
        game = Game(INITIAL_PIECES, mode=mode)
        running = True

        while running:
            clock.tick(FPS)

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
                                    print(winner)
                                    print(Game.AI)
                                    if winner or Game.AI:
                                        if winner == None:
                                            display_winner(screen, Game.AI)
                                            Game.AI = None
                                            running = False  # End game loop, return to menu
                                        else:
                                            display_winner(screen, winner)
                                            running = False  # End game loop, return to menu

            screen.fill((172, 60, 80))
            screen.blit(board_img, (0, BOARD_Y))

            for piece in game.pieces:
                piece.draw(screen, red_piece_img, blue_piece_img, red_king_img, blue_king_img)

            if game.selected_piece:
                pygame.draw.circle(screen, (255, 255, 0), (game.selected_piece.x, game.selected_piece.y), 35, 4)

            for tile in game.valid_moves:
                if tile != 'none':
                    x, y = TILE_POSITIONS[tile]
                    pygame.draw.circle(screen, (255, 255, 0), (x, y), 15)

            pygame.display.flip()

if __name__ == "__main__":
    main()
