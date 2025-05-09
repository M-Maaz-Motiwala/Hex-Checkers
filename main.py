# main.py

import pygame
import sys
from settings import *
from tilemap import TILE_POSITIONS, INITIAL_PIECES
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hexagon Checkers")

    board_img = pygame.image.load(BOARD_IMAGE_PATH)
    board_img = pygame.transform.scale(board_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    red_piece_img = pygame.image.load(RED_PIECE_IMAGE_PATH)
    blue_piece_img = pygame.image.load(BLUE_PIECE_IMAGE_PATH)

    red_piece_img = pygame.transform.scale(red_piece_img, (60, 60))
    blue_piece_img = pygame.transform.scale(blue_piece_img, (60, 60))

    clock = pygame.time.Clock()

    game = Game(INITIAL_PIECES)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_tile = None

                # Check which tile was clicked
                for tile, (tx, ty) in TILE_POSITIONS.items():
                    if (mx - tx) ** 2 + (my - ty) ** 2 <= 30 ** 2:
                        clicked_tile = tile
                        break

                if clicked_tile:
                    if game.selected_piece:
                        if game.move_selected_piece(clicked_tile):
                            print(f"Moved piece to {clicked_tile}")
                    else:
                        if game.select_piece(clicked_tile):
                            print(f"Selected {game.selected_piece.color} piece at {clicked_tile}")

        screen.fill((172, 60, 80))
        screen.blit(board_img, (0, 0))

        for piece in game.pieces:
            piece.draw(screen, red_piece_img, blue_piece_img)

        if game.selected_piece:
            pygame.draw.circle(screen, (255, 255, 0), (game.selected_piece.x, game.selected_piece.y), 35, 4)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
