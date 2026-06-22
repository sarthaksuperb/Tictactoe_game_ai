import os
import re
import unittest
from html.parser import HTMLParser

class HTMLStructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = []
        self.labels = []
        self.cells = []
        self.overlays = []
        self.win_lines = []
        self.reset_buttons = []
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Track input elements
        if tag == 'input':
            if attrs_dict.get('type') == 'radio' and attrs_dict.get('name') not in ('theme', 'game-mode'):
                self.inputs.append(attrs_dict)
                
        # Track label elements
        elif tag == 'label':
            self.labels.append(attrs_dict)
            
        # Track cell containers
        elif tag == 'div' and 'cell' in attrs_dict.get('class', ''):
            self.cells.append(attrs_dict)
            
        # Track overlays
        elif tag == 'div' and 'overlay' in attrs_dict.get('class', ''):
            self.overlays.append(attrs_dict)
            
        # Track win lines
        elif tag == 'div' and 'win-line' in attrs_dict.get('class', ''):
            self.win_lines.append(attrs_dict)
            
        # Track reset buttons
        elif tag == 'button' and attrs_dict.get('type') == 'reset':
            self.reset_buttons.append(attrs_dict)


class TestTicTacToeCSSGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_path = 'index.html'
        cls.css_path = 'style.css'
        
        # Read HTML
        with open(cls.html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
            
        # Read CSS
        with open(cls.css_path, 'r', encoding='utf-8') as f:
            cls.css_content = f.read()
            
        # Parse HTML
        cls.parser = HTMLStructureParser()
        cls.parser.feed(cls.html_content)

    def test_inputs_exist(self):
        """Verify that all 22 radio button inputs exist with proper IDs."""
        self.assertEqual(len(self.parser.inputs), 22, "Should have 22 radio button inputs (18 for game cells + 4 for difficulty levels)")
        
        # Check game cell inputs (18 total)
        for i in range(1, 10):
            id_x = f"cell-{i}-x"
            id_o = f"cell-{i}-o"
            
            # Find input with id_x
            input_x = next((inp for inp in self.parser.inputs if inp.get('id') == id_x), None)
            input_o = next((inp for inp in self.parser.inputs if inp.get('id') == id_o), None)
            
            self.assertIsNotNone(input_x, f"Input with ID '{id_x}' is missing.")
            self.assertIsNotNone(input_o, f"Input with ID '{id_o}' is missing.")
            self.assertEqual(input_x.get('name'), f"cell-{i}", f"Input '{id_x}' must share name 'cell-{i}' for grouping.")
            self.assertEqual(input_o.get('name'), f"cell-{i}", f"Input '{id_o}' must share name 'cell-{i}' for grouping.")
        
        # Check difficulty inputs
        difficulty_inputs = ['diff-easy', 'diff-medium', 'diff-hard', 'diff-expert']
        for diff_id in difficulty_inputs:
            diff_input = next((inp for inp in self.parser.inputs if inp.get('id') == diff_id), None)
            self.assertIsNotNone(diff_input, f"Difficulty input with ID '{diff_id}' is missing.")
            self.assertEqual(diff_input.get('type'), 'radio', f"Difficulty input '{diff_id}' must be a radio button.")
            self.assertEqual(diff_input.get('name'), 'difficulty', f"Difficulty input '{diff_id}' must have name 'difficulty'.")

    def test_grid_cells_exist(self):
        """Verify that all 9 cells exist in the grid board."""
        self.assertEqual(len(self.parser.cells), 9, "The board must contain exactly 9 grid cell containers.")
        for i in range(1, 10):
            cell_class = f"cell-{i}"
            cell = next((c for c in self.parser.cells if cell_class in c.get('class', '')), None)
            self.assertIsNotNone(cell, f"Grid cell '.{cell_class}' is missing.")

    def test_labels_match_inputs(self):
        """Verify that each cell contains labels pointing to the correct input IDs."""
        for i in range(1, 10):
            id_x = f"cell-{i}-x"
            id_o = f"cell-{i}-o"
            
            label_x = next((l for l in self.parser.labels if l.get('for') == id_x), None)
            label_o = next((l for l in self.parser.labels if l.get('for') == id_o), None)
            
            self.assertIsNotNone(label_x, f"Label pointing to '{id_x}' is missing.")
            self.assertIsNotNone(label_o, f"Label pointing to '{id_o}' is missing.")

    def test_win_lines_exist(self):
        """Verify that all 8 strike-through win line elements exist."""
        expected_lines = ['row-1', 'row-2', 'row-3', 'col-1', 'col-2', 'col-3', 'diag-1', 'diag-2']
        for line in expected_lines:
            line_found = any(line in l.get('class', '') for l in self.parser.win_lines)
            self.assertTrue(line_found, f"Win line '.win-line.{line}' is missing.")

    def test_overlays_exist(self):
        """Verify that victory and draw overlays exist."""
        win_overlay = next((o for o in self.parser.overlays if 'win-overlay' in o.get('class', '')), None)
        draw_overlay = next((o for o in self.parser.overlays if 'draw-overlay' in o.get('class', '')), None)
        
        self.assertIsNotNone(win_overlay, "Win overlay '.win-overlay' is missing.")
        self.assertIsNotNone(draw_overlay, "Draw overlay '.draw-overlay' is missing.")

    def test_reset_buttons_exist(self):
        """Verify that restart buttons are present in the form."""
        self.assertGreaterEqual(len(self.parser.reset_buttons), 1, "Should have at least 1 reset button in form.")

    def test_css_turn_indicators(self):
        """Verify that CSS contains turn indicators logic for all 0-8 moves."""
        # We check if style.css contains the general pattern for alternating turns
        # using the count of checked inputs.
        for i in range(1, 9):
            pattern = r"input\[name\^='cell-'\]:checked\s*~\s*" * i
            # Check if this sequence of inputs:checked exists in CSS
            match = re.search(pattern, self.css_content)
            self.assertIsNotNone(match, f"CSS turn indicator selector level {i} (matching cell inputs checked x{i}) is missing.")

    def test_css_win_conditions_overlay(self):
        """Verify that CSS contains all 16 victory overlay display selectors."""
        win_lines = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Cols
            (1, 5, 9), (3, 5, 7)              # Diagonals
        ]
        
        # Verify Player X and Player O rules
        for p in ['x', 'o']:
            for w in win_lines:
                # Build target search pattern for CSS
                # Example: #cell-1-x:checked ~ #cell-2-x:checked ~ #cell-3-x:checked
                parts = [f"#cell-{idx}-{p}:checked" for idx in w]
                # Join them with general sibling combinator "~" (allowing optional spaces)
                pattern = r"\s*~\s*".join(parts)
                match = re.search(pattern, self.css_content)
                self.assertIsNotNone(match, f"Win combination CSS selector for Player {p.upper()} lines {w} is missing.")

    def test_css_draw_overlay_hider(self):
        """Verify that CSS contains rules to override/hide the draw overlay if a player wins on the 9th move."""
        # Find if the draw overlay hide rules exist in the style sheet
        self.assertIn('.draw-overlay', self.css_content, "CSS should target '.draw-overlay'")
        # Ensure we have "display: none !important" in CSS
        self.assertIn('display: none !important', self.css_content, "CSS must declare 'display: none !important' to hide elements.")


if __name__ == '__main__':
    unittest.main()
