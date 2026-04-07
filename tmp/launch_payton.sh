#!/bin/bash
# launch_payton.sh - Helper script to launch payton.py cleanly in a new terminal

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Launching payton.py in a new terminal..."

# Find the default terminal emulator on Linux and run the script inside it
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "cd '$DIR' && echo 'Starting Payton Automation...' && ./run.sh payton.py; exec bash"
elif command -v konsole &> /dev/null; then
    konsole -e bash -c "cd '$DIR' && echo 'Starting Payton Automation...' && ./run.sh payton.py; exec bash"
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal -x bash -c "cd '$DIR' && echo 'Starting Payton Automation...' && ./run.sh payton.py; exec bash"
elif command -v x-terminal-emulator &> /dev/null; then
    x-terminal-emulator -e bash -c "cd '$DIR' && echo 'Starting Payton Automation...' && ./run.sh payton.py; exec bash"
else
    # Fallback if no known GUI terminal is found
    echo "Terminal emulator not found. Running in background."
    cd "$DIR" && ./run.sh payton.py &
fi
