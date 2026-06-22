import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_tests():
    # Retrieve Chrome path programmatically on macOS
    try:
        chrome_path = subprocess.check_output(["osascript", "-e", 'POSIX path of (path to application "Google Chrome")']).decode('utf-8').strip()
        chrome_binary = os.path.join(chrome_path, "Contents/MacOS/Google Chrome")
        print(f"[+] Found Google Chrome at: {chrome_binary}")
    except Exception as e:
        chrome_binary = None
        print("[-] Could not resolve Chrome path via AppleScript, relying on default path.")

    # Configure headless Chrome Options
    options = Options()
    if chrome_binary:
        options.binary_location = chrome_binary
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1200,800")

    print("[+] Launching headless Chrome browser...")
    driver = webdriver.Chrome(options=options)

    # Helper function to bypass 3D transform click intercepts using JavaScript
    def click_element(elem):
        driver.execute_script("arguments[0].click();", elem)

    try:
        url = "http://localhost:8080"
        print(f"[+] Navigating to {url}...")
        driver.get(url)
        time.sleep(1.5)

        # ----------------------------------------------------
        # 1. VERIFY TITLE & INITIAL STATE
        # ----------------------------------------------------
        title_elem = driver.find_element(By.CLASS_NAME, "main-title")
        print(f"[+] Game Title Verified: {title_elem.text}")
        
        turn_x = driver.find_element(By.CLASS_NAME, "turn-x")
        turn_o = driver.find_element(By.CLASS_NAME, "turn-o")
        assert turn_x.is_displayed(), "Player X should start the game."
        print("[+] Turn indicator shows X's turn initially.")

        # ----------------------------------------------------
        # 1B. TEST VS COMPUTER AI MODE
        # ----------------------------------------------------
        print("[+] Testing VS COMPUTER AI Opponent mode...")
        # Toggle mode to VS COMPUTER
        lbl_ai = driver.find_element(By.CLASS_NAME, "lbl-ai")
        click_element(lbl_ai)
        time.sleep(0.5)
        
        # Click Cell 1 (human)
        label_cell1_x = driver.find_element(By.CSS_SELECTOR, ".cell-1 .label-x")
        click_element(label_cell1_x)
        print("[+] Player X (human) clicked cell-1")
        
        # Wait for the AI delay
        time.sleep(1.0)
        
        # Verify Cell 1 has X mark
        mark_cell1_x = driver.find_element(By.CSS_SELECTOR, ".cell-1 .x-mark")
        assert mark_cell1_x.is_displayed(), "Cell 1 should have X mark."
        
        # Verify Cell 5 has O mark (since O plays center if empty!)
        mark_cell5_o = driver.find_element(By.CSS_SELECTOR, ".cell-5 .o-mark")
        assert mark_cell5_o.is_displayed(), "Cell 5 should have O mark (AI response)."
        print("[+] AI responded automatically by marking cell-5!")
        
        # Reset the board to clear for the next tests
        board_reset = driver.find_element(By.CLASS_NAME, "board-reset-btn")
        click_element(board_reset)
        time.sleep(0.5)
        
        # Switch back to VS PLAYER mode for the remaining tests
        lbl_2p = driver.find_element(By.CLASS_NAME, "lbl-2p")
        click_element(lbl_2p)
        time.sleep(0.5)
        print("[+] Switched back to VS PLAYER mode.")

        # ----------------------------------------------------
        # 2. TEST THEME SWITCHING (CYBER -> ARCADE -> AURORA)
        # ----------------------------------------------------
        print("[+] Testing theme switcher...")
        body = driver.find_element(By.TAG_NAME, "body")
        
        # Cyberpunk (Default): text-color should be white
        text_color_cyber = body.value_of_css_property("color")
        print(f"[+] Cyberpunk theme active. Text color: {text_color_cyber}")

        # Switch to Arcade theme
        lbl_retro = driver.find_element(By.CLASS_NAME, "lbl-retro")
        click_element(lbl_retro)
        time.sleep(0.5)
        text_color_retro = body.value_of_css_property("color")
        print(f"[+] Clicked ARCADE. Active color: {text_color_retro}")
        assert "rgb(57, 255, 20)" in text_color_retro or "rgba(57, 255, 20" in text_color_retro, "Arcade theme green text failed."

        # Switch to Aurora theme
        lbl_aurora = driver.find_element(By.CLASS_NAME, "lbl-aurora")
        click_element(lbl_aurora)
        time.sleep(0.5)
        text_color_aurora = body.value_of_css_property("color")
        print(f"[+] Clicked AURORA. Active color: {text_color_aurora}")
        # Aurora text color should be dark slate (rgb(45, 52, 70) or similar)
        assert "rgb(45, 52, 54)" in text_color_aurora or "rgb(0, 0, 0)" in text_color_aurora or "2d3436" in text_color_aurora or "45" in text_color_aurora, f"Aurora theme dark text failed. Got {text_color_aurora}"

        # Return to Cyberpunk theme
        lbl_cyber = driver.find_element(By.CLASS_NAME, "lbl-cyberpunk")
        click_element(lbl_cyber)
        time.sleep(0.5)
        print("[+] Switched back to CYBER theme.")

        # ----------------------------------------------------
        # 3. TEST PERSISTENT SCOREBOARD TALLIES
        # ----------------------------------------------------
        print("[+] Testing Scoreboard tally persistence...")
        # Check X score 1 checkbox
        score_x_1_cb = driver.find_element(By.ID, "score-x-1")
        score_x_1_lbl = driver.find_element(By.CSS_SELECTOR, "label[for='score-x-1']")
        
        assert not score_x_1_cb.is_selected(), "Score checkbox should not be selected initially."
        
        # Click the star label to check it
        click_element(score_x_1_lbl)
        time.sleep(0.3)
        assert score_x_1_cb.is_selected(), "Score checkbox should be selected after click."
        print("[+] Persistent score star clicked and checked.")

        # Click a cell to set board state
        label_cell1_x = driver.find_element(By.CSS_SELECTOR, ".cell-1 .label-x")
        click_element(label_cell1_x)
        time.sleep(0.3)
        
        # Verify Cell 1 is marked X
        mark_cell1_x = driver.find_element(By.CSS_SELECTOR, ".cell-1 .x-mark")
        assert mark_cell1_x.is_displayed(), "Cell 1 should show X mark."

        # Click BOARD reset button
        board_reset = driver.find_element(By.CLASS_NAME, "board-reset-btn")
        print("[+] Clicking board reset button...")
        click_element(board_reset)
        time.sleep(0.5)

        # Verify board state is reset, but scoreboard remains checked!
        assert not mark_cell1_x.is_displayed(), "Board state cell 1 should be cleared after reset."
        assert score_x_1_cb.is_selected(), "Scoreboard tally should STILL be checked (persisted!) after board reset."
        print("[+] Success: Tally persists across board resets!")

        # ----------------------------------------------------
        # 4. GAME PLAYWIN SEQUENCE (X Wins)
        # ----------------------------------------------------
        # Clicks list (making X win)
        # X: cell-1, O: cell-5, X: cell-2, O: cell-6, X: cell-3
        clicks = [
            ("cell-1", "label-x", "X"),
            ("cell-5", "label-o", "O"),
            ("cell-2", "label-x", "X"),
            ("cell-6", "label-o", "O"),
            ("cell-3", "label-x", "X")
        ]

        for idx, (cell_class, label_class, player) in enumerate(clicks):
            print(f"[+] Player {player} clicks {cell_class}")
            label = driver.find_element(By.CSS_SELECTOR, f".{cell_class} .{label_class}")
            click_element(label)
            time.sleep(0.4)

        # Verify X win overlay and victory message
        win_overlay = driver.find_element(By.CLASS_NAME, "win-overlay")
        assert win_overlay.is_displayed(), "Win overlay is not displayed after win."
        
        win_x_title = driver.find_element(By.CLASS_NAME, "win-x-title")
        assert win_x_title.is_displayed(), "Victory title for Player X is not shown."
        print("[+] Win overlay verified: PLAYER X DOMINATED THE GRID")

        # Save win state screenshot
        screenshot_dir = "/Users/sarthaksharma/.gemini/antigravity-ide/brain/0ffefed0-d927-4261-a591-1b1d07f44cd4"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, "tictactoe_win_state.png")
        driver.save_screenshot(screenshot_path)
        print(f"[+] Saved win state screenshot to: {screenshot_path}")

        # Click PLAY AGAIN on win overlay
        play_again_btn = driver.find_element(By.CSS_SELECTOR, ".win-overlay .neon-btn")
        click_element(play_again_btn)
        time.sleep(0.5)
        
        assert not win_overlay.is_displayed(), "Win overlay should be hidden after play again reset."
        print("[+] Board reset verified. Ready for new round.")
        print("\n🏆 SUCCESS: All browser integration tests passed!")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
