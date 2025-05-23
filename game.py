# game.py

from pieces import Piece
from tilemap import TILE_POSITIONS, RED_TILE_NEIGHBORS, BLUE_TILE_NEIGHBORS, KING_TILE_NEIGHBORS
import copy
import random  # move this to the top of the file

class Game:
    AI = None
    def __init__(self, initial_pieces, mode, simulation = False):
        self.simulation = simulation
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
            # print(f"Invalid move to {to_tile}")
            return False
        if self.tile_occupancy[to_tile] is not None:
            # print(f"Tile {to_tile} is occupied!")
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
                self.pieces.remove(captured_piece)
                self.tile_occupancy[jumped_tile] = None


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
                # print(f"Further jumps available: {further_jumps}")
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
            Game.AI = 'blue'
            return "blue"
        if self.turn == "blue" and not blue_moves:
            print("Red wins! Blue has no valid moves.")
            Game.AI = 'red'
            return "red"

        return None

    def end_turn(self):
        self.selected_piece = None
        self.valid_moves = []
        self.turn = "blue" if self.turn == "red" else "red"

        if (self.mode == "pvcpu_easy") and self.turn == "blue" and not self.simulation:
            self.ai_move_easy()
        elif (self.mode == "pvcpu_hard") and self.turn == "blue" and not self.simulation:
            self.ai_move_hard()

    def ai_move_easy(self):
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
            winner = self.check_game_over()
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

    def ai_move_hard(self):
        print("AI is thinking (Minimax)...")
        depth = 3  # You can adjust this based on desired difficulty

        score, from_tile, to_tile = self.minimax_ABP(depth, is_maximizing=True, alpha=float('-inf'), beta=float('inf'))

        if from_tile is None or to_tile is None:
            # print("AI has no valid moves.")
            self.end_turn()
            return

        ai_piece = self.tile_occupancy[from_tile]
        self.selected_piece = ai_piece
        self.valid_moves = self.get_valid_moves(from_tile)

        print(f"AI moves from {from_tile} to {to_tile} (Score: {score})")
        self.move_selected_piece(to_tile)
         # Perform additional jumps if available
        while self.selected_piece and self.valid_moves:
            print(f"AI continues multi-jump from {self.selected_piece.position}")
            next_jump = self.valid_moves[0]  # Just take the first valid jump for now
            self.move_selected_piece(next_jump)
            
    def minimax_ABP(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        winner = self.check_game_over()
        if winner == "blue":
            return (float('inf'), None, None)
        elif winner == "red":
            return (float('-inf'), None, None)
        elif depth == 0:
            return (self.evaluate_board(), None, None)

        current_color = "blue" if is_maximizing else "red"
        pieces = [p for p in self.pieces if p.color == current_color]

        best_score = float('-inf') if is_maximizing else float('inf')
        best_move = (None, None)

        for piece in pieces:
            valid_moves = self.get_valid_moves(piece.position)
            for move in valid_moves:
                sim_game = copy.deepcopy(self)
                sim_game.simulation = True
                sim_piece = sim_game.tile_occupancy[piece.position]
                sim_game.selected_piece = sim_piece
                sim_game.valid_moves = sim_game.get_valid_moves(piece.position)
                moved = sim_game.move_selected_piece(move)

                if not moved:
                    continue

                score, _, _ = sim_game.minimax_ABP(depth - 1, not is_maximizing, alpha, beta)

                if is_maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = (piece.position, move)
                    alpha = max(alpha, best_score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (piece.position, move)
                    beta = min(beta, best_score)

                # 💡 Alpha-Beta Pruning step
                if beta <= alpha:
                    break  # Prune remaining branches

        return best_score, best_move[0], best_move[1]
        
    
    def evaluate_board(self):
        red_score = sum(2 if p.is_king else 1 for p in self.pieces if p.color == "red")
        blue_score = sum(2 if p.is_king else 1 for p in self.pieces if p.color == "blue")
        return blue_score - red_score  # Positive means good for blue (AI)
