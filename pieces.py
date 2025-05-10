# piece.py

from tilemap import TILE_POSITIONS

class Piece:
    def __init__(self, color, position, is_king = False):
        self.color = color
        self.position = position
        self.x, self.y = TILE_POSITIONS[position]
        self.is_king = is_king  # 🟢 NEW: track king status

    def move_to(self, new_position):
        self.position = new_position
        self.x, self.y = TILE_POSITIONS[new_position]

    def draw(self, screen, red_img, blue_img, red_king_img, blue_king_img):
        if self.is_king:
            img = red_king_img if self.color == "red" else blue_king_img
        else:
            img = red_img if self.color == "red" else blue_img
            
        screen.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))
