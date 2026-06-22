# 🪐 Cyber Neon Tic-Tac-Toe (Hybrid CSS Engine)

An ultra-premium, interactive, and responsive Tic-Tac-Toe game featuring three high-fidelity theme skins, a 3D perspective hover-tilt effect, and an unbeatable AI opponent.

👉 **[Play the Live Demo Here!](https://sarthaksuperb.github.io/Tictactoe_game_ai/)**

---

## 🎨 Design Aesthetics & Themes

The game features three completely unique visual skins utilizing modern CSS variables and advanced styling tokens:

1. **Cyberpunk Neon (Default)**: Glowing Electric Cyan (`#00f3ff`) and Hot Pink/Magenta (`#ff007f`) marks against a deep glassmorphic backdrop.
2. **Retro Arcade**: CRT-style scanline overlay with faint flickering animations, glowing green amber text, and pixelated font styling.
3. **Aurora Light**: A soothing light-mode skin with a pastel peach/purple gradient background and soft rounded shadows.

---

## ⚡ Technical Highlights

### 1. CSS-Driven Turn & Board State
* **No JS turn tracking**: Board state and player turn cycles are tracked entirely via checkboxes/radio buttons and the general sibling selector (`~`).
* **Persistent Scoreboards**: Score tallies are managed via checkboxes outside the primary board form. Toggling "Play Again" clears the board inputs but retains the scoreboard.

### 2. 3D Tilt Effect
* Utilizes the modern CSS `:has()` relational selector to compute hover locations and dynamically tilt the 3D-perspective game board towards the player's cursor.
* Uses `transform: translateZ(...)` for depth layers on marks (X and O).

### 3. Minimax AI Opponent (VS Computer)
* When **VS COMPUTER** mode is activated, an intelligent JavaScript actor listens for turn checkboxes.
* Evaluates the unbeatable Minimax game-tree solver to automatically make moves for Player O.
* Features a built-in **500ms thinking delay** with CSS indicator states to mimic human gameplay response times.

---

## 🛠️ Local Development & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarthaksuperb/Tictactoe_game_ai.git
   cd Tictactoe_game_ai
   ```

2. **Run a local development server:**
   ```bash
   python3 -m http.server 8080
   ```
   Open `http://localhost:8080` in your web browser.

3. **Run Automated Tests:**
   * Unit tests: `python3 test_game.py`
   * E2E Selenium Integration tests: `./run_selenium_tests.sh`

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
