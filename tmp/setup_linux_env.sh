#!/bin/bash
# setup_linux_env.sh - Setup development environment for remote Linux laptop

echo "🚀 Setting up the Remote Environment for Brain Battle..."

# 1. Close existing VS Code windows ONLY if there are no unsaved changes
echo "1️⃣  Closing existing VS Code windows gracefully..."
# wmctrl sends a close request (like clicking the 'X'). If there are unsaved files, VS Code will block and prompt you.
if command -v wmctrl &> /dev/null; then
    # Close all windows titled 'Visual Studio Code'
    wmctrl -c "Visual Studio Code" || echo "No VS Code windows to close."
else
    echo "wmctrl not found, skipping VS Code graceful close (install with 'sudo apt install wmctrl')."
fi
sleep 2

# 2. Launch Zen Browser (opening GitHub or Dev Space)
echo "2️⃣  Launching Zen Browser..."
# We will use 'zen-browser' executable or default to xdg-open if it exists
if command -v zen-browser &> /dev/null; then
    zen-browser "https://github.com/Brain-Battle-App" &
elif command -v zen &> /dev/null; then
    zen "https://github.com/Brain-Battle-App" &
else
    echo "Zen browser not found in PATH. Please run it manually."
fi
sleep 2

# 3. Launch VS Code with brain-battle codebase
echo "3️⃣  Launching VS Code with brain-battle codebase..."
# Change this path to where brain-battle is stored if it's different on the Linux machine
BRAIN_BATTLE_DIR="$HOME/Documents/CODING_PROJECTS/WORK/brain-battle/brain-battle" 

if command -v code &> /dev/null; then
    if [ -d "$BRAIN_BATTLE_DIR" ]; then
        code "$BRAIN_BATTLE_DIR"
    else
        # Try guessing from common locations
        if [ -d "$HOME/Desktop/brain-battle" ]; then
            code "$HOME/Desktop/brain-battle"
        elif [ -d "$HOME/Documents/brain-battle" ]; then
            code "$HOME/Documents/brain-battle"
        else
            echo "Could not find brain-battle directory. Opening VS Code in current directory."
            code .
        fi
    fi
else
    echo "VS Code 'code' command not found."
fi
sleep 2

# 4. Launch payton.py via helper script
echo "4️⃣  Launching payton.py Activity Automation..."
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELPER_SCRIPT="$DIR/launch_payton.sh"

if [ -f "$HELPER_SCRIPT" ]; then
    chmod +x "$HELPER_SCRIPT"
    "$HELPER_SCRIPT"
else
    echo "launch_payton.sh script not found. Trying to run ./run.sh payton.py directly..."
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd '$DIR' && ./run.sh payton.py; exec bash"
    elif command -v x-terminal-emulator &> /dev/null; then
        x-terminal-emulator -e bash -c "cd '$DIR' && ./run.sh payton.py; exec bash"
    else
        echo "Please run ./run.sh payton.py manually in a new terminal."
    fi
fi

echo "✅ Environment setup process finished!"
