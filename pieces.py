# piece.py

from tilemap import TILE_POSITIONS

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.x, self.y = TILE_POSITIONS[position]

    def move_to(self, new_position):
        self.position = new_position
        self.x, self.y = TILE_POSITIONS[new_position]

    def draw(self, screen, red_img, blue_img):
        img = red_img if self.color == "red" else blue_img
        screen.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))
