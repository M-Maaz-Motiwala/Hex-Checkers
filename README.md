# Hex-Checkers/Draught: A Strategic AI Game on a Hexagonal Board

**Group Members:**
- Muhammad Maaz Motiwala 22k-4402
- Javeria 22k-4399
- Taha Alam 22k-4425

**Course:** Artificial Intelligence  
**Instructor:** Talha Shahid  
**Submission Date:** May 11, 2025

## Abstract

This project presents **Hex-Checkers/Draught**, a digital adaptation of the classic Checkers/Draught (Checkers) game implemented on a hexagonal grid using Python and Pygame. The project integrates Artificial Intelligence (AI) employing the **Minimax algorithm** with **Alpha-Beta pruning** for decision-making. The final implementation includes three playable modes: **Player vs Player**, **Player vs NPC (Easy)**, and **Player vs NPC (Hard)**. The aim was to create an engaging AI-driven board game experience while experimenting with AI search algorithms in a modified strategic environment.

## 1. Introduction

Checkers/Draught is a historically significant strategy game that traditionally uses an 8×8 square grid. This project reimagines the classic game by introducing a hexagonal board layout that preserves core mechanics such as diagonal movement, capturing, and kinging, while introducing unique tactical challenges. The objective of this project was to not only implement the game’s mechanics on a hexagonal board but also to integrate an AI opponent capable of making strategic moves based on established AI algorithms.

## 2. Project Objectives

- To develop a playable, interactive Checkers/Draught game on a hexagonal board.
- To design and implement AI opponents with varying difficulty levels.
- To integrate the **Minimax algorithm** with **Alpha-Beta pruning** for efficient AI decision-making.
- To create a visually intuitive game environment using **Pygame**.

## 3. Game Modes

The final version of **Hex-Checkers/Draught** offers three gameplay modes:
1. **Player vs Player**: Two human players alternate turns on the same device.
2. **Player vs NPC (Easy)**: The AI opponent looks for the current gain, basically having a depth of 1.
3. **Player vs NPC (Hard)**: The AI opponent uses a deeper Minimax search with Alpha-Beta pruning, resulting in more calculated, strategic gameplay.

> **Note:** The core movement and capture mechanics remain consistent across all modes.

## 4. AI Methodology

The AI component was developed using the **Minimax algorithm**, enhanced with **Alpha-Beta pruning** to optimize the search space. The AI evaluates potential moves based on a heuristic function that considers:
- Number of remaining pieces for each player.
- Number of kings for each player.

## 5. Game Rules and Mechanics

- **Board Layout**: A hexagonal grid with adjusted diagonal movement and capturing based on neighboring hex cells.
- **Movement**: Pieces move to adjacent hexagonal cells in diagonal directions.
- **Capturing**: Mandatory captures are enforced. Multiple captures are allowed if available.
- **Kinging**: A piece is promoted to ‘King’ upon reaching the opponent’s baseline.
- **Winning Conditions**: A player wins by either eliminating all opponent pieces or leaving them with no legal moves.

## 6. Implementation Details

- **Programming Language**: Python
- **Libraries**:
  - **Pygame**: For game rendering, event handling, and animations.
  - **Python standard libraries**: For AI logic, data structures, and control flow.
  
- **Game Rendering**:  
  A hexagonal board was rendered using Pygame’s graphical capabilities. Mouse-based selection and movement highlighting were implemented for an interactive user experience.

- **AI Integration**:  
  The AI operates asynchronously during its turn, computing the optimal move via the Minimax algorithm before updating the board state.

## 7. Results and Observations

- The AI’s performance and decision-making complexity scaled appropriately with increased search depth.
- The hard mode AI demonstrated effective defensive and offensive strategies, while easy mode maintained basic move selection.
- The hexagonal layout introduced unique movement patterns and strategic depth compared to traditional Checkers/Draught.

## 8. Challenges Faced

- Adapting traditional Checkers/Draught movement and capturing rules to a hexagonal grid.
- Optimizing AI performance to maintain reasonable response times, especially at higher search depths.
- Designing a user-friendly interface for an unconventional board structure.

## 9. Conclusion

**Hex-Checkers/Draught** successfully integrates strategic AI gameplay within a reimagined classic game environment. By implementing Minimax with Alpha-Beta pruning and offering varying AI difficulties, the project highlights the application of classical AI search techniques in a novel board layout. This project serves as a practical demonstration of AI’s role in strategic game development and problem-solving.

## 10. How to Run

1. Clone the repository: git clone https://github.com/M-Maaz-Motiwala/Hex-Checkers.git
2. Install Pygame.
3. Run the game:


## 11. License

This project is licensed under the MIT License.

## 12. Acknowledgements

- Special thanks to our instructor **Talha Shahid** for guidance.
- Thanks to the Pygame community for providing resources to implement this project.
