# game.py

from pieces import Piece
from tilemap import TILE_POSITIONS, RED_TILE_NEIGHBORS, BLUE_TILE_NEIGHBORS, KING_TILE_NEIGHBORS

class Game:
    def __init__(self, initial_pieces):
        self.pieces = []
        self.tile_occupancy = {pos: None for pos in TILE_POSITIONS}

        for pos, color in initial_pieces.items():
            piece = Piece(color, pos)
            self.pieces.append(piece)
            self.tile_occupancy[pos] = piece

        self.selected_piece = None

    def select_piece(self, tile):
        piece = self.tile_occupancy.get(tile)
        if piece:
            self.selected_piece = piece
            return True
        return False

    def move_selected_piece(self, to_tile):
        if not self.selected_piece:
            return False
        if self.tile_occupancy[to_tile] is not None:
            print(f"Tile {to_tile} is occupied!")
            return False

        from_tile = self.selected_piece.position

        # Update piece position
        self.selected_piece.move_to(to_tile)

        # Update tile occupancy map
        self.tile_occupancy[from_tile] = None
        self.tile_occupancy[to_tile] = self.selected_piece

        self.selected_piece = None
        return True

    def get_valid_moves(self, from_tile):
        piece = self.tile_occupancy[from_tile]
        if piece is None:
            return []

        if hasattr(piece, 'is_king') and piece.is_king:
            neighbor_map = KING_TILE_NEIGHBORS
        elif piece.color == "red":
            neighbor_map = RED_TILE_NEIGHBORS
        else:
            neighbor_map = BLUE_TILE_NEIGHBORS

        valid_moves = []
        neighbors = neighbor_map.get(from_tile, [])
        for to_tile in neighbors:
            if self.tile_occupancy[to_tile] is None:
                valid_moves.append(to_tile)

        return valid_moves
