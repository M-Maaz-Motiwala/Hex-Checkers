# game.py

from pieces import Piece
from tilemap import TILE_POSITIONS, RED_TILE_NEIGHBORS, BLUE_TILE_NEIGHBORS, KING_TILE_NEIGHBORS
import copy

class Game:
    def __init__(self, initial_pieces, mode):
        self.mode = mode
        self.turn = "red"
        self.pieces = []
        self.tile_occupancy = {pos: None for pos in TILE_POSITIONS}

        for pos, color in initial_pieces.items():
            piece = Piece(color, pos)
            self.pieces.append(piece)
            self.tile_occupancy[pos] = piece

        self.selected_piece = None
        self.valid_moves = []

    def select_piece(self, tile):
        piece = self.tile_occupancy.get(tile)
        if piece and piece.color == self.turn:
            if self.selected_piece == piece:
                self.selected_piece = None
                self.valid_moves = []
                return False
            else:
                self.selected_piece = piece
                self.valid_moves = self.get_valid_moves(tile)
                return True
        return False

    def move_selected_piece(self, to_tile):
        if not self.selected_piece or to_tile not in self.valid_moves:
            print(f"Invalid move to {to_tile}")
            return False
        if self.tile_occupancy[to_tile] is not None:
            print(f"Tile {to_tile} is occupied!")
            return False

        from_tile = self.selected_piece.position
        neighbors = KING_TILE_NEIGHBORS if self.selected_piece.is_king else (
            RED_TILE_NEIGHBORS if self.selected_piece.color == "red" else BLUE_TILE_NEIGHBORS
        )

        jumped_tile = None
        for idx, neighbor in enumerate(neighbors.get(from_tile, [])):
            if neighbor == "none" or self.tile_occupancy.get(neighbor) is None:
                continue
            enemy_piece = self.tile_occupancy[neighbor]
            if enemy_piece.color == self.selected_piece.color:
                continue

            beyond_neighbors = neighbors.get(neighbor, [])
            if idx < len(beyond_neighbors):
                landing_tile = beyond_neighbors[idx]
                if landing_tile == to_tile and self.tile_occupancy.get(landing_tile) is None:
                    jumped_tile = neighbor
                    break

        if jumped_tile:
            captured_piece = self.tile_occupancy[jumped_tile]
            if captured_piece:
                print(f"Captured {captured_piece.color} piece at {jumped_tile}")
                self.pieces.remove(captured_piece)
                self.tile_occupancy[jumped_tile] = None

        print(f"Attempting to move piece from {from_tile} to {to_tile}")

        self.selected_piece.move_to(to_tile)
        self.tile_occupancy[from_tile] = None
        self.tile_occupancy[to_tile] = self.selected_piece

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

        if jumped_tile:
            further_jumps = self.get_valid_jumps(to_tile)
            if further_jumps:
                self.selected_piece = self.tile_occupancy[to_tile]
                self.valid_moves = further_jumps
                print(f"Further jumps available: {further_jumps}")
            else:
                self.end_turn()
        else:
            self.end_turn()

        winner = self.check_game_over()
        if winner:
            print(f"🎉 Game Over! {winner.capitalize()} wins!")

        return True

    def get_valid_moves(self, from_tile):
        valid_moves = []
        piece = self.tile_occupancy.get(from_tile)
        if not piece:
            return valid_moves

        neighbors_map = KING_TILE_NEIGHBORS if piece.is_king else (
            RED_TILE_NEIGHBORS if piece.color == 'red' else BLUE_TILE_NEIGHBORS
        )
        neighbors = neighbors_map.get(from_tile, [])

        for idx, neighbor in enumerate(neighbors):
            if neighbor == "none":
                continue
            neighbor_piece = self.tile_occupancy.get(neighbor)
            if neighbor_piece is None:
                valid_moves.append(neighbor)
            elif neighbor_piece.color != piece.color:
                beyond_neighbors = neighbors_map.get(neighbor, [])
                if idx < len(beyond_neighbors):
                    landing_tile = beyond_neighbors[idx]
                    if landing_tile != "none" and self.tile_occupancy.get(landing_tile) is None:
                        valid_moves.append(landing_tile)
        print(f"Valid moves for {piece.color} piece at {from_tile}: {valid_moves}")

        return valid_moves

    def get_valid_jumps(self, from_tile):
        piece = self.tile_occupancy[from_tile]
        if piece is None:
            return []

        neighbor_map = KING_TILE_NEIGHBORS if piece.is_king else (
            RED_TILE_NEIGHBORS if piece.color == "red" else BLUE_TILE_NEIGHBORS
        )
        enemy_color = "blue" if piece.color == "red" else "red"

        valid_jumps = []
        neighbors = neighbor_map.get(from_tile, [])
        for idx, neighbor in enumerate(neighbors):
            neighbor_piece = self.tile_occupancy.get(neighbor)
            if neighbor_piece and neighbor_piece.color == enemy_color:
                beyond_neighbors = neighbor_map.get(neighbor, [])
                if idx < len(beyond_neighbors):
                    beyond_tile = beyond_neighbors[idx]
                    if beyond_tile != "none" and self.tile_occupancy.get(beyond_tile) is None:
                        valid_jumps.append(beyond_tile)

        return valid_jumps

    def check_game_over(self):
        red_pieces = [p for p in self.pieces if p.color == "red"]
        blue_pieces = [p for p in self.pieces if p.color == "blue"]

        if not red_pieces:
            print("Blue wins! All red pieces captured.")
            return "blue"
        if not blue_pieces:
            print("Red wins! All blue pieces captured.")
            return "red"

        red_moves = any(self.get_valid_moves(p.position) for p in red_pieces)
        blue_moves = any(self.get_valid_moves(p.position) for p in blue_pieces)

        if self.turn == "red" and not red_moves:
            print("Blue wins! Red has no valid moves.")
            return "blue"
        if self.turn == "blue" and not blue_moves:
            print("Red wins! Blue has no valid moves.")
            return "red"

        return None

    def end_turn(self):
        self.selected_piece = None
        self.valid_moves = []
        self.turn = "blue" if self.turn == "red" else "red"

        if self.mode == "pvcpu" and self.turn == "blue":
            self.ai_move()

    import random

    def ai_move(self):
        print("AI is thinking...")

        blue_pieces = [p for p in self.pieces if p.color == "blue"]
        all_moves = []

        for piece in blue_pieces:
            valid_moves = self.get_valid_moves(piece.position)
            for move in valid_moves:
                simulated_game = copy.deepcopy(self)
                simulated_piece = simulated_game.tile_occupancy[piece.position]
                simulated_game.selected_piece = simulated_piece
                simulated_game.valid_moves = simulated_game.get_valid_moves(piece.position)
                
                if simulated_game.move_selected_piece(move):
                    gain = len(self.pieces) - len(simulated_game.pieces)
                    all_moves.append((gain, piece.position, move))

        if not all_moves:
            print("AI has no valid moves. Skipping turn.")
            self.end_turn()
            return

        # Pick move with maximum gain
        all_moves.sort(reverse=True)
        best_move = all_moves[0]
        from_tile, to_tile = best_move[1], best_move[2]

        # Execute the move directly
        ai_piece = self.tile_occupancy[from_tile]
        self.selected_piece = ai_piece
        self.valid_moves = self.get_valid_moves(from_tile)

        print(f"AI moves from {from_tile} to {to_tile}")
        self.move_selected_piece(to_tile)


    