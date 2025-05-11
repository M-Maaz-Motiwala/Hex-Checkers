# piece.py

# from tilemap import TILE_POSITIONS

# class Piece:
#     def __init__(self, color, position, is_king = False):
#         self.color = color
#         self.position = position
#         self.x, self.y = TILE_POSITIONS[position]
#         self.is_king = is_king  # 🟢 NEW: track king status

#     def move_to(self, new_position):
#         self.position = new_position
#         self.x, self.y = TILE_POSITIONS[new_position]

#     def draw(self, screen, red_img, blue_img, red_king_img, blue_king_img):
#         if self.is_king:
#             img = red_king_img if self.color == "red" else blue_king_img
#         else:
#             img = red_img if self.color == "red" else blue_img
            
#         screen.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))


import pygame
from tilemap import TILE_POSITIONS

class Piece:
    def __init__(self, color, position, is_king=False):
        self.color = color
        self.position = position
        self.x, self.y = TILE_POSITIONS[position]
        self.is_king = is_king

    def move_to(self, new_position):
        self.position = new_position
        self.x, self.y = TILE_POSITIONS[new_position]

    def draw(self, screen, red_img, blue_img, red_king_img, blue_king_img, is_selected=False):
        # Select image
        if self.is_king:
            img = red_king_img if self.color == "red" else blue_king_img
        else:
            img = red_img if self.color == "red" else blue_img

        # Center coordinates
        img_rect = img.get_rect(center=(self.x, self.y))

        # # Draw drop shadow (offset + alpha)
        # shadow = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        # pygame.draw.circle(shadow, (110, 50, 40, 100), (img.get_width() // 2, img.get_height() // 2), img.get_width() // 2)
        # screen.blit(shadow, (img_rect.x + 3, img_rect.y + 3))  # Shadow offset

        # Draw actual piece
        screen.blit(img, img_rect.topleft)

        # Optional glow for selection
        if is_selected:
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 35, 4)
