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
        self.valid_moves = []  # 🟡 ADD THIS LINE

    def select_piece(self, tile):
        piece = self.tile_occupancy.get(tile)
        if piece:
            if self.selected_piece == piece:
                self.selected_piece = None
                self.valid_moves = []
                return False
            else:
                self.selected_piece = piece
                self.valid_moves = self.get_valid_moves(tile)  # 🟡 GET valid moves
                return True
        return False
    
    def move_selected_piece(self, to_tile):
        if not self.selected_piece:
            return False
        if to_tile not in self.valid_moves:  # 🟢 ADD THIS LINE
            print(f"Invalid move: {to_tile} is not a valid neighbor!")
            return False
        if self.tile_occupancy[to_tile] is not None:
            print(f"Tile {to_tile} is occupied!")
            return False

        from_tile = self.selected_piece.position

        if self.selected_piece.is_king:
            neighbors = KING_TILE_NEIGHBORS
        else:
            neighbors = RED_TILE_NEIGHBORS if self.selected_piece.color == "red" else BLUE_TILE_NEIGHBORS


        # neighbors = RED_TILE_NEIGHBORS if self.selected_piece.color == "red" else BLUE_TILE_NEIGHBORS
        # Check if this move is a jump
        jumped_tile = None

        for idx, neighbor in enumerate(neighbors.get(from_tile, [])):
            if neighbor == "none" or self.tile_occupancy.get(neighbor) is None:
                continue  # no enemy here, or invalid neighbor
            enemy_piece = self.tile_occupancy.get(neighbor)
            if enemy_piece.color == self.selected_piece.color:
                continue  # same color, can't capture own piece

            beyond_neighbors = neighbors.get(neighbor, [])
            if idx >= len(beyond_neighbors):
                continue  # no neighbor in this direction
            landing_tile = beyond_neighbors[idx]
            if landing_tile == to_tile and self.tile_occupancy.get(landing_tile) is None:
                jumped_tile = neighbor
                break


        # REMOVE captured piece if a jump happened
        if jumped_tile:
            captured_piece = self.tile_occupancy.get(jumped_tile)
            if captured_piece:
                print(f"Captured {captured_piece.color} piece at {jumped_tile}")
                self.pieces.remove(captured_piece)
                self.tile_occupancy[jumped_tile] = None

        # Move the piece
        self.selected_piece.move_to(to_tile)
        self.tile_occupancy[from_tile] = None
        self.tile_occupancy[to_tile] = self.selected_piece
        
        # 🟢 KING PROMOTION CHECK
        red_king_tiles = {"A3", "B5", "C7"}
        blue_king_tiles = {"C1", "D1", "F1"}
        
        if self.selected_piece.color == "red" and to_tile in red_king_tiles:
            if not self.selected_piece.is_king:
                self.selected_piece.is_king = True
                print(f"Red piece at {to_tile} became a KING!")
        elif self.selected_piece.color == "blue" and to_tile in blue_king_tiles:
            if not self.selected_piece.is_king:
                self.selected_piece.is_king = True
                print(f"Blue piece at {to_tile} became a KING!")

        # 🟢 Check for possible further jumps from the new position
        further_jumps = self.get_valid_jumps(to_tile)
        if further_jumps:
            self.selected_piece = self.tile_occupancy[to_tile]
            self.valid_moves = further_jumps
            print(f"Further jumps available: {further_jumps}")
        else:
            self.selected_piece = None
            self.valid_moves = []

        return True

    def get_valid_moves(self, from_tile):
        valid_moves = []
        piece = self.tile_occupancy.get(from_tile)
        if not piece:
            return valid_moves

        neighbors_map = KING_TILE_NEIGHBORS if piece.is_king else (RED_TILE_NEIGHBORS if piece.color == 'red' else BLUE_TILE_NEIGHBORS)
        neighbors = neighbors_map.get(from_tile, [])

        for idx, neighbor in enumerate(neighbors):
            if neighbor == "none":
                continue

            neighbor_piece = self.tile_occupancy.get(neighbor)

            if neighbor_piece is None:
                # normal move
                valid_moves.append(neighbor)
            elif neighbor_piece.color != piece.color:
                # enemy → check beyond
                beyond_neighbors = neighbors_map.get(neighbor, [])
                if idx >= len(beyond_neighbors):
                    continue  # no beyond position
                landing_tile = beyond_neighbors[idx]
                if landing_tile != "none" and self.tile_occupancy.get(landing_tile) is None:
                    # valid capture
                    valid_moves.append(landing_tile)

        return valid_moves  
    
    
    def get_valid_jumps(self, from_tile):
        piece = self.tile_occupancy[from_tile]
        if piece is None:
            return []

        neighbor_map = KING_TILE_NEIGHBORS if getattr(piece, 'is_king', False) else (RED_TILE_NEIGHBORS if piece.color == "red" else BLUE_TILE_NEIGHBORS)
        enemy_color = "blue" if piece.color == "red" else "red"

        valid_jumps = []
        neighbors = neighbor_map.get(from_tile, [])
        for idx, neighbor in enumerate(neighbors):
            neighbor_piece = self.tile_occupancy.get(neighbor)
            if neighbor_piece and neighbor_piece.color == enemy_color:
                beyond_neighbors = neighbor_map.get(neighbor, [])
                if idx < len(beyond_neighbors):
                    beyond_tile = beyond_neighbors[idx]
                    if beyond_tile and self.tile_occupancy.get(beyond_tile) is None:
                        valid_jumps.append(beyond_tile)

        return valid_jumps

        