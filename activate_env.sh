#!/bin/bash

VENV_DIR=".venv"

echo "------------------------------------------------"
echo "Initializing Weather Project Environment..."
echo "------------------------------------------------"

# 1. Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: 'uv' is not installed."
    echo "Install it via: curl -LsSf https://astral.sh/uv/install.sh | sh"
    return 1 2>/dev/null || exit 1
fi

# 2. Sync the environment (Forcing Python 3.11 as per our PySpark requirement)
echo "Checking dependencies and syncing with Python 3.11..."
# Lệnh này đảm bảo uv dùng 3.11 để tạo venv
uv sync --python 3.11

# 3. Activate the virtual environment
if [ -d "$VENV_DIR" ]; then
    # Dùng lệnh này để bọc an toàn cho cả bash và zsh
    source "$VENV_DIR/bin/activate"
    
    echo "SUCCESS: Virtual environment activated."
    echo "Python location: $(which python)"
    echo "Python version:  $(python --version)"
    echo "------------------------------------------------"
else
    echo "ERROR: Failed to create or find the virtual environment at $VENV_DIR"
    return 1 2>/dev/null || exit 1
fi