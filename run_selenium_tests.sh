#!/bin/bash
set -e

# Change directory to script folder location
cd "$(dirname "$0")"

echo "=========================================="
echo "🎯 STARTING BROWSER INTEGRATION TESTS"
echo "=========================================="

# Create local python virtual environment to isolate dependencies
if [ ! -d ".test-venv" ]; then
    echo "[*] Creating python virtual environment '.test-venv'..."
    python3 -m venv .test-venv
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source .test-venv/bin/activate

# Install Selenium
echo "[*] Installing Selenium in virtual environment..."
pip install --quiet --upgrade pip
pip install --quiet selenium

# Check if HTTP server is running on 8080
if ! lsof -i :8080 -t >/dev/null; then
    echo "[*] Local HTTP server not detected. Starting background server..."
    python3 -m http.server 8080 &
    SERVER_PID=$!
    sleep 2
else
    echo "[*] Local HTTP server is already running on port 8080."
    SERVER_PID=""
fi

# Run the selenium script
echo "[*] Executing browser tests..."
python3 selenium_test.py

# Cleanup server if we started it
if [ -n "$SERVER_PID" ]; then
    echo "[*] Shutting down background HTTP server (PID: $SERVER_PID)..."
    kill "$SERVER_PID"
fi

# Deactivate virtual environment
echo "[*] Deactivating virtual environment..."
deactivate

echo "=========================================="
echo "✅ TESTS COMPLETED SUCCESSFULLY"
echo "=========================================="
