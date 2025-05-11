# tilemap.py
from settings import *
# Manually define the clickable tiles' pixel positions
# Example: {"A1": (x, y), "A2": (x, y), ...}

TILE_POSITIONS = {
    "A1": (310, 60+BOARD_Y),
    "A2": (440, 60+BOARD_Y),
    "A3": (570, 60+BOARD_Y),

    "B1": (190, 186.25+BOARD_Y),
    "B2": (310, 186.25+BOARD_Y),
    "B3": (440, 186.25+BOARD_Y),
    "B4": (570, 186.25+BOARD_Y),
    "B5": (690, 186.25+BOARD_Y),

    "C1": (65, 312.5+BOARD_Y),
    "C2": (190, 312.5+BOARD_Y),
    "C3": (310, 312.5+BOARD_Y),
    "C4": (440, 312.5+BOARD_Y),
    "C5": (570, 312.5+BOARD_Y),
    "C6": (690, 312.5+BOARD_Y),
    "C7": (820, 312.5+BOARD_Y),

    "D1": (190, 438.75+BOARD_Y),
    "D2": (310, 438.75+BOARD_Y),
    "D3": (440, 438.75+BOARD_Y),
    "D4": (570, 438.75+BOARD_Y),
    "D5": (690, 438.75+BOARD_Y),

    "F1": (310, 565+BOARD_Y),
    "F2": (440, 565+BOARD_Y),
    "F3": (570, 565+BOARD_Y),
}

# Define neighbors (simple adjacency; customize for hex if needed)
RED_TILE_NEIGHBORS = {
    # "Piece_position": [0, 1]
    "A1": ["none", "A2"],
    "A2": ["none", "A3"],
    "A3": ["none", "none"],

    "B1": ["none", "B2"],
    "B2": ["A1", "B3"],
    "B3": ["A2", "B4"],
    "B4": ["A3", "B5"],
    "B5": ["none", "none"],

    "C1": ["none", "C2"],
    "C2": ["B1", "C3"],
    "C3": ["B2", "C4"],
    "C4": ["B3", "C5"],
    "C5": ["B4", "C6"],
    "C6": ["B5", "C7"],
    "C7": ["none", "none"],

    "D1": ["C2", "D2"],
    "D2": ["C3", "D3"],
    "D3": ["C4", "D4"],
    "D4": ["C5", "D5"],
    "D5": ["C6", "none"],

    "F1": ["D2", "F2"],
    "F2": ["D3", "F3"],
    "F3": ["D4", "none"]
}

BLUE_TILE_NEIGHBORS = {
    # "Piece_position": [0, 1]
    "A1": ["B2", "none"],
    "A2": ["B3", "A1"],
    "A3": ["B4", "A2"],

    "B1": ["C2", "none"],
    "B2": ["C3", "B1"],
    "B3": ["C4", "B2"],
    "B4": ["C5", "B3"],
    "B5": ["C6", "B4"],

    "C1": ["none", "none"],
    "C2": ["D1", "C1"],
    "C3": ["D2", "C2"],
    "C4": ["D3", "C3"],
    "C5": ["D4", "C4"],
    "C6": ["D5", "C5"],
    "C7": ["none","C6"],

    "D1": ["none", "none"],
    "D2": ["F1", "D1"],
    "D3": ["F2", "D2"],
    "D4": ["F3", "D3"],
    "D5": ["none", "D4"],

    "F1": ["none", "none"],
    "F2": ["none", "F1"],
    "F3": ["none", "F2"]
}

KING_TILE_NEIGHBORS = {
    # 'piece_position' : [0,1,2,3]
    "A1": ["none", "none", "A2", "B2"],
    "A2": ["none", "A1", "A3", "B3"],
    "A3": ["none", "A2", "none", "B4"],

    "B1": ["none", "none", "B2", "C2"],
    "B2": ["A1", "B1", "B3", "C3"],
    "B3": ["A2", "B2", "B4", "C4"],
    "B4": ["A3", "B3", "B5", "C5"],
    "B5": ["none", "B4", "none", "C6"],

    "C1": ["none", "none", "C2", "none"],
    "C2": ["B1", "C1", "C3", "D1"],
    "C3": ["B2", "C2", "C4", "D2"],
    "C4": ["B3", "C3", "C5", "D3"],
    "C5": ["B4", "C4", "C6", "D4"],
    "C6": ["B5", "C5", "C7", "D5"],
    "C7": ["none", "C6", "none", "none"],

    "D1": ["C2", "none", "D2", "none"],
    "D2": ["C3", "D1", "D3", "F1"],
    "D3": ["C4", "D2", "D4", "F2"],
    "D4": ["C5", "D3", "D5", "F3"],
    "D5": ["C6", "D4", "none", "none"],

    "F1": ["D2", "none", "F2", "none"],
    "F2": ["D3", "F1", "F3", "none"],
    "F3": ["D4", "F2", "none", "none"]
}

INITIAL_PIECES = {
    "C1": "red",
    "D1": "red",
    "F1": "red",
    "C2": "red",
    "D2": "red",
    "F2": "red",

    "A3": "blue",
    "B5": "blue",
    "C7": "blue",
    "A2": "blue",
    "B4": "blue",
    "C6": "blue",
}
