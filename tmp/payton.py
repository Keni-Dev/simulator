#!/usr/bin/env python3
"""
Upwork Activity Automation Script v2.3
=======================================
Maintains HIGH activity levels for Upwork time tracking by simulating
human-like mouse movements, keyboard activity, and browser browsing.

Features:
- Toggle on/off with Scroll Lock, F9, or Ctrl+Shift+X
- Randomized mouse/keyboard activity (20-150 KB, 15-70 Mouse per minute)
- VS Code file switching every ~10 minutes
- Terminal commands every 10-15 minutes
- Browser activity every 8-12 minutes (GitHub PRs, code, docs)
- Dual editor pane support (Ctrl+1/Ctrl+2)
- Working directory cache
- Fail-safe: Move mouse to any screen corner to stop

Requirements:
    pip install pyautogui pynput
    System: xdotool (pacman -S xdotool)
"""

import pyautogui
import random
import time
import threading
import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from pynput import keyboard

# ============================================================================
# CONFIGURATION
# ============================================================================

TOGGLE_KEY = keyboard.Key.scroll_lock
# F9 or Ctrl+Shift+X as backup combo for Mac Remote Desktop

# Activity targets per minute
MIN_KEYBOARD_PER_MINUTE = 20
MAX_KEYBOARD_PER_MINUTE = 150
MIN_MOUSE_PER_MINUTE = 15
MAX_MOUSE_PER_MINUTE = 70

# Interval configs (seconds)
FILE_SWITCH_INTERVAL = 600         # ~10 min
TERMINAL_MIN_INTERVAL = 600        # 10 min
TERMINAL_MAX_INTERVAL = 900        # 15 min
BROWSER_MIN_INTERVAL = 480         # 8 min
BROWSER_MAX_INTERVAL = 720         # 12 min
BROWSER_STAY_MIN = 120             # 4 min in browser
BROWSER_STAY_MAX = 240             # 8 min in browser

# Config cache
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.payton_config.json')

# GitHub repo URL
GITHUB_REPO = "https://github.com/Brain-Battle-App/brain-battle"
#GITHUB_REPO = "https://github.com/Brain-Battle-App/battle-backend/"

# GitHub static pages (non-code)
GITHUB_STATIC_PAGES = [
    f"{GITHUB_REPO}",
    f"{GITHUB_REPO}/pulls",
    f"{GITHUB_REPO}/issues",
    f"{GITHUB_REPO}/actions",
    f"{GITHUB_REPO}/commits/main",
    f"{GITHUB_REPO}/branches",
]

# Documentation URLs to browse (all verified working)
DOC_URLS = [
    # React Native Core Components (verified)
    "https://reactnative.dev/docs/getting-started",
    "https://reactnative.dev/docs/components-and-apis",
    "https://reactnative.dev/docs/flatlist",
    "https://reactnative.dev/docs/sectionlist",
    "https://reactnative.dev/docs/view",
    "https://reactnative.dev/docs/text",
    "https://reactnative.dev/docs/scrollview",
    "https://reactnative.dev/docs/touchableopacity",
    "https://reactnative.dev/docs/pressable",
    "https://reactnative.dev/docs/image",
    "https://reactnative.dev/docs/textinput",
    "https://reactnative.dev/docs/stylesheet",
    "https://reactnative.dev/docs/button",
    "https://reactnative.dev/docs/switch",
    "https://reactnative.dev/docs/modal",
    "https://reactnative.dev/docs/statusbar",
    "https://reactnative.dev/docs/keyboardavoidingview",
    "https://reactnative.dev/docs/activityindicator",
    # React Native APIs (verified)
    "https://reactnative.dev/docs/animated",
    "https://reactnative.dev/docs/dimensions",
    "https://reactnative.dev/docs/linking",
    "https://reactnative.dev/docs/alert",
    "https://reactnative.dev/docs/performance",
    "https://reactnative.dev/docs/debugging",
    "https://reactnative.dev/docs/animations",
    "https://reactnative.dev/docs/gesture-responder-system",
    # Expo Core (verified)
    "https://docs.expo.dev/",
    "https://docs.expo.dev/router/introduction/",
    "https://docs.expo.dev/router/navigating-between-pages/",
    "https://docs.expo.dev/router/navigation-layouts/",
    "https://docs.expo.dev/develop/development-builds/introduction/",
    "https://docs.expo.dev/build/introduction/",
    "https://docs.expo.dev/eas-update/introduction/",
    # Expo SDK Modules (verified)
    "https://docs.expo.dev/versions/latest/sdk/camera/",
    "https://docs.expo.dev/versions/latest/sdk/notifications/",
    "https://docs.expo.dev/versions/latest/sdk/splash-screen/",
    "https://docs.expo.dev/versions/latest/sdk/font/",
    "https://docs.expo.dev/versions/latest/sdk/securestore/",
    "https://docs.expo.dev/versions/latest/sdk/linear-gradient/",
    "https://docs.expo.dev/versions/latest/sdk/haptics/",
    "https://docs.expo.dev/versions/latest/sdk/av/",
    "https://docs.expo.dev/versions/latest/sdk/constants/",
    "https://docs.expo.dev/versions/latest/sdk/file-system/",
    "https://docs.expo.dev/versions/latest/sdk/async-storage/",
    # TypeScript Handbook (verified)
    "https://www.typescriptlang.org/docs/handbook/intro.html",
    "https://www.typescriptlang.org/docs/handbook/2/everyday-types.html",
    "https://www.typescriptlang.org/docs/handbook/2/functions.html",
    "https://www.typescriptlang.org/docs/handbook/2/objects.html",
    "https://www.typescriptlang.org/docs/handbook/2/classes.html",
    "https://www.typescriptlang.org/docs/handbook/2/modules.html",
    "https://www.typescriptlang.org/docs/handbook/2/types-from-types.html",
    "https://www.typescriptlang.org/docs/handbook/2/generics.html",
    "https://www.typescriptlang.org/docs/handbook/utility-types.html",
    "https://www.typescriptlang.org/docs/handbook/2/narrowing.html",
    "https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html",
    "https://www.typescriptlang.org/docs/handbook/2/conditional-types.html",
    "https://www.typescriptlang.org/docs/handbook/2/mapped-types.html",
    "https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html",
    # Turso (verified)
    "https://docs.turso.tech/",
    "https://docs.turso.tech/sdk/ts/quickstart",
    "https://docs.turso.tech/sdk/ts/reference",
    "https://docs.turso.tech/features/embedded-replicas/introduction",
    "https://docs.turso.tech/cli/overview",
    # Firebase (verified)
    "https://firebase.google.com/docs",
    "https://firebase.google.com/docs/auth",
    "https://firebase.google.com/docs/firestore",
    "https://firebase.google.com/docs/cloud-messaging",
    "https://firebase.google.com/docs/functions",
    "https://firebase.google.com/docs/storage",
    "https://firebase.google.com/docs/analytics",
    "https://firebase.google.com/docs/remote-config",
    # React Navigation (commonly used with RN)
    "https://reactnavigation.org/docs/getting-started",
    "https://reactnavigation.org/docs/stack-navigator",
    "https://reactnavigation.org/docs/tab-based-navigation",
    "https://reactnavigation.org/docs/drawer-based-navigation",
    "https://reactnavigation.org/docs/nesting-navigators",
]

# Tween functions for human-like mouse curves
TWEEN_FUNCTIONS = [
    pyautogui.easeInQuad,
    pyautogui.easeOutQuad,
    pyautogui.easeInOutQuad,
    pyautogui.easeInOutSine,
    pyautogui.easeInBounce,
    pyautogui.easeOutBounce,
    pyautogui.linear,
]

# Terminal commands (NPM/TS/mobile dev focused)
TERMINAL_COMMANDS = [
    'git status', 'git log --oneline -5', 'git log --oneline -10',
    'git branch', 'git branch -a', 'git diff --stat',
    'git stash list', 'git remote -v', 'git fetch --dry-run',
    'npm list --depth=0 2>/dev/null || yarn list --depth=0 2>/dev/null',
    'npm outdated 2>/dev/null || yarn outdated 2>/dev/null',
    'npm run 2>/dev/null | head -20',
    'yarn --version 2>/dev/null || npm --version',
    'npx expo --version 2>/dev/null || echo "checking expo..."',
    'npx tsc --noEmit 2>/dev/null | head -20',
    'npx eslint --ext .ts,.tsx src/ 2>/dev/null | head -10',
    'cat tsconfig.json 2>/dev/null | head -30',
    'adb devices 2>/dev/null || echo "checking devices..."',
    'ls -la',
    'ls -la src/ 2>/dev/null || ls -la app/ 2>/dev/null || ls -la',
    'pwd',
    'find . -name "*.tsx" -type f | head -15',
    'find . -name "*.ts" -type f | head -15',
    'cat package.json | head -40',
    'cat package.json | grep -A 20 "dependencies"',
    'cat package.json | grep -A 10 "scripts"',
    'grep -r "TODO" --include="*.tsx" . 2>/dev/null | head -5',
    'grep -r "FIXME" --include="*.ts" . 2>/dev/null | head -5',
    'grep -rn "useState" --include="*.tsx" . 2>/dev/null | head -8',
    'grep -rn "useEffect" --include="*.tsx" . 2>/dev/null | head -8',
    'node --version',
    'npm test -- --listTests 2>/dev/null | head -10',
    'cat README.md 2>/dev/null | head -40',
    'history | tail -10',
    'df -h | head -3',
    'tree -L 2 src/ 2>/dev/null || ls -R src/ 2>/dev/null | head -30',
]

SAFE_MARGIN = 100
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.02

CODE_EXTENSIONS = {
    '.ts', '.tsx', '.js', '.jsx', '.json', '.yaml', '.yml',
    '.css', '.scss', '.html', '.xml',
    '.swift', '.kt', '.java', '.gradle',
    '.py', '.sh', '.bash'
}

# ============================================================================
# WINDOW MANAGEMENT (xdotool)
# ============================================================================

def find_window(name_pattern: str) -> str:
    """Find a window ID by name pattern using xdotool."""
    try:
        result = subprocess.run(
            ['xdotool', 'search', '--name', name_pattern],
            capture_output=True, text=True, timeout=3
        )
        window_ids = result.stdout.strip().split('\n')
        if window_ids and window_ids[0]:
            return window_ids[0]  # Return first match
    except Exception:
        pass
    return None

def activate_window(window_id: str) -> bool:
    """Activate (focus) a window by its ID."""
    try:
        subprocess.run(
            ['xdotool', 'windowactivate', window_id],
            capture_output=True, timeout=3
        )
        return True
    except Exception:
        return False

def focus_browser():
    """Switch focus to Zen Browser."""
    # Try multiple patterns that might match Zen Browser
    for pattern in ['Zen Browser', 'zen', 'Mozilla', 'brain-battle']:
        wid = find_window(pattern)
        if wid:
            activate_window(wid)
            log("🌐 Focused browser window")
            time.sleep(0.5)
            return True
    log("⚠️ Browser window not found")
    return False

def focus_vscode():
    """Switch focus to VS Code."""
    for pattern in ['Visual Studio Code', 'Code']:
        wid = find_window(pattern)
        if wid:
            activate_window(wid)
            log("📝 Focused VS Code window")
            time.sleep(0.5)
            return True
    log("⚠️ VS Code window not found")
    return False

# ============================================================================
# CONFIG PERSISTENCE
# ============================================================================

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass

def get_last_directory():
    config = load_config()
    return config.get('last_directory', os.getcwd())

def save_last_directory(directory):
    config = load_config()
    config['last_directory'] = directory
    save_config(config)

# ============================================================================
# GLOBAL STATE
# ============================================================================

class AutomationState:
    def __init__(self):
        self.is_paused = True
        self.should_stop = False
        self.end_time = None
        self.last_file_switch = None
        self.last_terminal_activity = None
        self.last_browser_activity = None
        self.current_project_files = []
        self.current_file_line_count = 100
        self.lock = threading.Lock()
        self.minute_start = None
        self.keyboard_count = 0
        self.mouse_count = 0
        self.target_keyboard = 0
        self.target_mouse = 0

state = AutomationState()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def log(message: str, show_counts: bool = False):
    timestamp = datetime.now().strftime("%H:%M:%S")
    status = "▶️ ACTIVE" if not state.is_paused else "⏸️ PAUSED"
    if show_counts:
        print(f"[{timestamp}] [{status}] {message} | KB: {state.keyboard_count}/{state.target_keyboard} | M: {state.mouse_count}/{state.target_mouse}")
    else:
        print(f"[{timestamp}] [{status}] {message}")

def get_screen_size():
    return pyautogui.size()

def get_safe_position():
    width, height = get_screen_size()
    return (
        random.randint(SAFE_MARGIN, width - SAFE_MARGIN),
        random.randint(SAFE_MARGIN, height - SAFE_MARGIN)
    )

def get_file_line_count(file_path: str) -> int:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 100

def scan_project_files(start_path=None):
    if start_path is None:
        start_path = os.getcwd()
    code_files = []
    try:
        for root, dirs, files in os.walk(start_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
                'node_modules', '__pycache__', 'venv', 'env', '.venv',
                'dist', 'build', '.git', '.svn', 'vendor', 'target',
                'android', 'ios', '.expo', '.next'
            }]
            for f in files:
                # Skip icon files (SVG wrappers, not useful for browsing)
                if 'icon' in f.lower() or 'Icon' in f:
                    continue
                ext = Path(f).suffix.lower()
                if ext in CODE_EXTENSIONS:
                    code_files.append(os.path.join(root, f))
            if len(code_files) >= 100:
                break
    except Exception as e:
        log(f"Scan error: {e}")
    return code_files

# ============================================================================
# MINUTE ACTIVITY MANAGER
# ============================================================================

def reset_minute_targets():
    state.minute_start = datetime.now()
    state.keyboard_count = 0
    state.mouse_count = 0
    state.target_keyboard = random.randint(MIN_KEYBOARD_PER_MINUTE, MAX_KEYBOARD_PER_MINUTE)
    state.target_mouse = random.randint(MIN_MOUSE_PER_MINUTE, MAX_MOUSE_PER_MINUTE)
    log(f"📊 New minute | Target: KB={state.target_keyboard}, Mouse={state.target_mouse}")

def is_new_minute():
    if state.minute_start is None:
        return True
    return (datetime.now() - state.minute_start).total_seconds() >= 60

def should_do_keyboard():
    return state.keyboard_count < state.target_keyboard

def should_do_mouse():
    return state.mouse_count < state.target_mouse

def get_remaining_time_in_minute():
    if state.minute_start is None:
        return 60
    return max(0, 60 - (datetime.now() - state.minute_start).total_seconds())

# ============================================================================
# KEYBOARD ACTIONS
# ============================================================================

def human_pause():
    """Random micro-pause to simulate human thinking/reading."""
    if random.random() < 0.15:  # 15% chance of a thinking pause
        time.sleep(random.uniform(0.5, 2.0))
    elif random.random() < 0.3:  # 30% chance of a quick glance pause
        time.sleep(random.uniform(0.1, 0.4))

def kb_arrow_press():
    human_pause()
    pyautogui.press(random.choice(['up', 'down', 'left', 'right']))
    state.keyboard_count += 1

def kb_arrow_burst():
    """Burst of arrow keys with variable speed (fast scan, slow at interesting parts)."""
    key = random.choice(['up', 'down', 'left', 'right'])
    count = random.randint(3, 12)
    # Variable speed: start fast, maybe slow down in middle, speed up again
    for i in range(count):
        if state.keyboard_count >= state.target_keyboard:
            break
        pyautogui.press(key)
        state.keyboard_count += 1
        # Variable delay - sometimes fast scanning, sometimes slow reading
        if random.random() < 0.2:  # 20% chance of slow-down (reading something)
            time.sleep(random.uniform(0.15, 0.4))
        else:
            time.sleep(random.uniform(0.02, 0.08))

def kb_page_nav():
    human_pause()
    pyautogui.press(random.choice(['pageup', 'pagedown']))
    state.keyboard_count += 1
    # Small pause after page nav (eyes adjusting to new content)
    time.sleep(random.uniform(0.3, 0.8))

def kb_home_end():
    pyautogui.press(random.choice(['home', 'end']))
    state.keyboard_count += 1

def kb_ctrl_arrow():
    pyautogui.hotkey('ctrl', random.choice(['left', 'right']))
    state.keyboard_count += 2

def kb_extra_arrows():
    """Extra arrows with natural rhythm variation."""
    key = random.choice(['up', 'down', 'left', 'right'])
    for _ in range(random.randint(2, 5)):
        pyautogui.press(key)
        state.keyboard_count += 1
        time.sleep(random.uniform(0.02, 0.12))  # More variable timing

def kb_escape():
    pyautogui.press('escape')
    state.keyboard_count += 1
    time.sleep(random.uniform(0.2, 0.5))  # Brief pause after escape

def kb_goto_line():
    max_line = min(state.current_file_line_count, 500)
    if max_line < 10:
        max_line = 50
    line = str(random.randint(1, max_line))
    pyautogui.hotkey('ctrl', 'g')
    state.keyboard_count += 2
    time.sleep(0.15)
    pyautogui.typewrite(line, interval=0.04)
    state.keyboard_count += len(line)
    time.sleep(0.1)
    pyautogui.press('enter')
    state.keyboard_count += 1

def kb_file_start_end():
    if random.random() < 0.5:
        pyautogui.hotkey('ctrl', 'home')
    else:
        pyautogui.hotkey('ctrl', 'end')
    state.keyboard_count += 2

def kb_switch_editor_pane():
    pane = random.choice(['1', '2'])
    pyautogui.hotkey('ctrl', pane)
    state.keyboard_count += 2

KB_ACTIONS = [
    (kb_arrow_burst, 35),
    (kb_arrow_press, 25),
    (kb_page_nav, 15),
    (kb_ctrl_arrow, 10),
    (kb_home_end, 5),
    (kb_extra_arrows, 4),
    (kb_switch_editor_pane, 3),
    (kb_file_start_end, 2),
    (kb_goto_line, 1),
]

# ============================================================================
# MOUSE ACTIONS (with human-like tween curves)
# ============================================================================

def get_tween():
    """Get a random tween function for natural mouse movement."""
    return random.choice(TWEEN_FUNCTIONS)

def mouse_small_move():
    """Small mouse movement with natural curve."""
    cx, cy = pyautogui.position()
    w, h = get_screen_size()
    nx = max(SAFE_MARGIN, min(w - SAFE_MARGIN, cx + random.randint(-80, 80)))
    ny = max(SAFE_MARGIN, min(h - SAFE_MARGIN, cy + random.randint(-60, 60)))
    pyautogui.moveTo(nx, ny, duration=random.uniform(0.08, 0.25), tween=get_tween())
    state.mouse_count += 1

def mouse_medium_move():
    """Medium mouse movement with curved path."""
    cx, cy = pyautogui.position()
    w, h = get_screen_size()
    nx = max(SAFE_MARGIN, min(w - SAFE_MARGIN, cx + random.randint(-200, 200)))
    ny = max(SAFE_MARGIN, min(h - SAFE_MARGIN, cy + random.randint(-150, 150)))
    pyautogui.moveTo(nx, ny, duration=random.uniform(0.15, 0.4), tween=get_tween())
    state.mouse_count += 1

def mouse_scroll():
    """Single scroll with variable speed."""
    human_pause()
    pyautogui.scroll(random.randint(1, 4) * random.choice([-1, 1]))
    state.mouse_count += 1

def mouse_scroll_burst():
    """Scroll burst simulating reading - variable speed as eyes scan."""
    direction = random.choice([-1, 1])
    for i in range(random.randint(2, 6)):
        if state.mouse_count >= state.target_mouse:
            break
        pyautogui.scroll(direction * random.randint(1, 3))
        state.mouse_count += 1
        # Variable pauses: sometimes fast scroll, sometimes stop to read
        if random.random() < 0.25:
            time.sleep(random.uniform(0.5, 1.5))  # Pausing to read something
        else:
            time.sleep(random.uniform(0.1, 0.35))

def mouse_jitter():
    """Natural hand micro-tremor movements."""
    for _ in range(random.randint(2, 5)):
        if state.mouse_count >= state.target_mouse:
            break
        dx = random.gauss(0, 5)  # Gaussian distribution = more natural
        dy = random.gauss(0, 5)
        pyautogui.moveRel(int(dx), int(dy), duration=random.uniform(0.01, 0.04))
        state.mouse_count += 1
        time.sleep(random.uniform(0.02, 0.1))

def mouse_move_to_random():
    """Move to random position with natural curve and overshoot."""
    x, y = get_safe_position()
    duration = random.uniform(0.25, 0.6)
    pyautogui.moveTo(x, y, duration=duration, tween=get_tween())
    state.mouse_count += 1
    # Small overshoot correction (humans don't land perfectly)
    if random.random() < 0.4:
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.moveRel(
            random.randint(-8, 8), random.randint(-8, 8),
            duration=random.uniform(0.03, 0.08)
        )
        state.mouse_count += 1

def mouse_hover_pause():
    """Move mouse and pause (simulating reading/hovering over element)."""
    cx, cy = pyautogui.position()
    w, h = get_screen_size()
    nx = max(SAFE_MARGIN, min(w - SAFE_MARGIN, cx + random.randint(-120, 120)))
    ny = max(SAFE_MARGIN, min(h - SAFE_MARGIN, cy + random.randint(-80, 80)))
    pyautogui.moveTo(nx, ny, duration=random.uniform(0.1, 0.3), tween=get_tween())
    state.mouse_count += 1
    # Hover/read pause
    time.sleep(random.uniform(0.5, 2.0))

MOUSE_ACTIONS = [
    (mouse_small_move, 25),
    (mouse_scroll_burst, 25),
    (mouse_scroll, 15),
    (mouse_jitter, 12),
    (mouse_hover_pause, 10),   # NEW: hover & read
    (mouse_medium_move, 8),
    (mouse_move_to_random, 5),
]

# ============================================================================
# ACTION DISPATCHER
# ============================================================================

def pick_weighted(actions):
    total = sum(w for _, w in actions)
    r = random.randint(1, total)
    cumulative = 0
    for action, weight in actions:
        cumulative += weight
        if r <= cumulative:
            return action
    return actions[0][0]

def perform_keyboard_action():
    try:
        pick_weighted(KB_ACTIONS)()
    except Exception as e:
        log(f"KB error: {e}")

def perform_mouse_action():
    try:
        pick_weighted(MOUSE_ACTIONS)()
    except Exception as e:
        log(f"Mouse error: {e}")

# ============================================================================
# FILE SWITCHING
# ============================================================================

def action_open_file():
    if not state.current_project_files:
        state.current_project_files = scan_project_files()
    if state.current_project_files:
        fp = random.choice(state.current_project_files)
        fn = os.path.basename(fp)
        state.current_file_line_count = get_file_line_count(fp)
        pyautogui.hotkey('ctrl', 'p')
        state.keyboard_count += 2
        time.sleep(0.25)
        pyautogui.typewrite(fn, interval=0.03)
        state.keyboard_count += len(fn)
        time.sleep(0.15)
        pyautogui.press('enter')
        state.keyboard_count += 1
        log(f"📁 Opened: {fn} ({state.current_file_line_count} lines)")
        time.sleep(0.3)
        pyautogui.scroll(random.randint(-8, 8))
        state.mouse_count += 1

def maybe_switch_file():
    now = datetime.now()
    if state.last_file_switch is None:
        state.last_file_switch = now
        return
    elapsed = (now - state.last_file_switch).total_seconds()
    if elapsed >= FILE_SWITCH_INTERVAL + random.randint(-90, 90):
        log("📂 Switching file...")
        state.current_project_files = scan_project_files()
        action_open_file()
        state.last_file_switch = now

# ============================================================================
# TERMINAL INTERACTION
# ============================================================================

def do_terminal_activity():
    log("💻 Terminal activity...")
    pyautogui.hotkey('ctrl', '`')
    state.keyboard_count += 2
    time.sleep(0.5)

    for cmd in random.sample(TERMINAL_COMMANDS, random.randint(1, 3)):
        pyautogui.typewrite(cmd, interval=random.uniform(0.03, 0.07))
        state.keyboard_count += len(cmd)
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.press('enter')
        state.keyboard_count += 1
        log(f"💻 $ {cmd}")
        time.sleep(random.uniform(1.0, 3.0))
        if random.random() < 0.3:
            pyautogui.scroll(random.randint(-3, 3))
            state.mouse_count += 1
            time.sleep(0.3)

    time.sleep(random.uniform(0.5, 1.5))
    pyautogui.hotkey('ctrl', random.choice(['1', '2']))
    state.keyboard_count += 2
    time.sleep(0.3)
    log("💻 Back to editor")

def maybe_terminal_activity():
    now = datetime.now()
    if state.last_terminal_activity is None:
        state.last_terminal_activity = now
        return
    elapsed = (now - state.last_terminal_activity).total_seconds()
    if elapsed >= random.randint(TERMINAL_MIN_INTERVAL, TERMINAL_MAX_INTERVAL):
        try:
            do_terminal_activity()
        except Exception as e:
            log(f"Terminal error: {e}")
        finally:
            state.last_terminal_activity = datetime.now()

# ============================================================================
# BROWSER INTERACTION
# ============================================================================

def browser_scroll_page():
    """Heavy scroll for GitHub pages (code files, PRs, commits)."""
    scroll_actions = random.randint(5, 15)
    for _ in range(scroll_actions):
        if state.is_paused or state.should_stop:
            return
        direction = random.choice([-1, -1, -1, 1])  # Mostly scroll down (reading)
        amount = random.randint(1, 4) * direction
        pyautogui.scroll(amount)
        state.mouse_count += 1
        time.sleep(random.uniform(0.3, 1.2))

        # Occasionally move mouse (looking at different parts)
        if random.random() < 0.3:
            mouse_small_move()

        # Occasionally press arrow keys
        if random.random() < 0.2:
            pyautogui.press(random.choice(['down', 'down', 'up']))
            state.keyboard_count += 1

def browser_scroll_docs():
    """Gentle scroll for documentation pages (shorter content, more reading)."""
    scroll_actions = random.randint(2, 4)
    for _ in range(scroll_actions):
        if state.is_paused or state.should_stop:
            return
        # Small gentle scrolls - docs pages aren't that long
        amount = random.randint(1, 2) * random.choice([-1, -1, 1])
        pyautogui.scroll(amount)
        state.mouse_count += 1
        # Longer pauses between scrolls (actually reading the text)
        time.sleep(random.uniform(1.5, 4.0))

        # Occasionally move mouse to a code block or link
        if random.random() < 0.25:
            mouse_small_move()
            time.sleep(random.uniform(0.5, 1.5))

def browser_navigate_url(url: str, page_type: str = 'github'):
    """Open a URL in a new tab, browse it for 60-90s, then close the tab.
    page_type: 'github' for heavy scrolling, 'docs' for gentle scrolling.
    """
    log(f"🌐 Navigating to: {url[:60]}...")

    # Open new tab
    pyautogui.hotkey('ctrl', 't')
    state.keyboard_count += 2
    time.sleep(0.5)

    # Type URL in address bar (Ctrl+L is already focused in new tab)
    pyautogui.typewrite(url, interval=random.uniform(0.02, 0.05))
    state.keyboard_count += len(url)
    time.sleep(0.2)

    pyautogui.press('enter')
    state.keyboard_count += 1

    # Wait for page to load
    time.sleep(random.uniform(2.0, 4.0))

    # Stay on this page for at least 60-90 seconds
    page_stay = random.uniform(60, 90)
    page_end = time.time() + page_stay
    log(f"🌐 Reading page ({page_type}) for ~{page_stay:.0f}s...")

    while time.time() < page_end and not state.is_paused and not state.should_stop:
        if page_type == 'docs':
            # Docs: gentle scroll, longer reading pauses
            browser_scroll_docs()
            if time.time() < page_end:
                time.sleep(random.uniform(8.0, 15.0))  # Longer reading pauses
        else:
            # GitHub: heavier scrolling through code
            browser_scroll_page()
            if time.time() < page_end:
                time.sleep(random.uniform(3.0, 8.0))

        # Occasionally move mouse to a link/element (hovering)
        if random.random() < 0.3:
            mouse_small_move()
            time.sleep(random.uniform(1.0, 3.0))

    # Close this tab (goes back to previous tab)
    pyautogui.hotkey('ctrl', 'w')
    state.keyboard_count += 2
    time.sleep(0.3)

def browser_switch_tabs():
    """Switch between existing browser tabs."""
    num_switches = random.randint(1, 3)
    for _ in range(num_switches):
        pyautogui.hotkey('ctrl', 'tab')
        state.keyboard_count += 2
        time.sleep(random.uniform(1.0, 2.5))
        # Scroll the current tab a bit
        for _ in range(random.randint(2, 5)):
            pyautogui.scroll(random.choice([-2, -1, 1]))
            state.mouse_count += 1
            time.sleep(random.uniform(0.3, 0.8))

def get_github_file_url():
    """Build a GitHub URL from an actual project file in the working directory."""
    if not state.current_project_files:
        state.current_project_files = scan_project_files()
    
    if state.current_project_files:
        file_path = random.choice(state.current_project_files)
        # Convert absolute path to relative path from project root
        try:
            rel_path = os.path.relpath(file_path, os.getcwd())
            return f"{GITHUB_REPO}/blob/main/{rel_path}"
        except Exception:
            pass
    return f"{GITHUB_REPO}"

def get_github_folder_url():
    """Build a GitHub URL from an actual folder in the working directory."""
    if not state.current_project_files:
        state.current_project_files = scan_project_files()
    
    # Get unique directories from project files
    dirs = set()
    for fp in state.current_project_files:
        try:
            rel = os.path.relpath(os.path.dirname(fp), os.getcwd())
            if rel and rel != '.':
                # Get top-level and second-level folders
                parts = rel.split(os.sep)
                dirs.add(parts[0])
                if len(parts) >= 2:
                    dirs.add(os.path.join(parts[0], parts[1]))
        except Exception:
            pass
    
    if dirs:
        folder = random.choice(list(dirs))
        return f"{GITHUB_REPO}/tree/main/{folder}"
    return f"{GITHUB_REPO}"

def browser_review_github():
    """Simulate reviewing GitHub - PRs, code files, folders, commits."""
    activity = random.choices(
        ['scroll_repo', 'check_pulls', 'browse_file', 'browse_folder',
         'view_commits', 'browse_tabs', 'static_page'],
        weights=[15, 20, 25, 15, 10, 10, 5],
        k=1
    )[0]

    if activity == 'scroll_repo':
        log("🌐 Scrolling repo main page...")
        browser_scroll_page()

    elif activity == 'check_pulls':
        browser_navigate_url(f"{GITHUB_REPO}/pulls")

    elif activity == 'browse_file':
        url = get_github_file_url()
        browser_navigate_url(url)

    elif activity == 'browse_folder':
        url = get_github_folder_url()
        browser_navigate_url(url)

    elif activity == 'view_commits':
        browser_navigate_url(f"{GITHUB_REPO}/commits/main")

    elif activity == 'browse_tabs':
        browser_switch_tabs()

    elif activity == 'static_page':
        url = random.choice(GITHUB_STATIC_PAGES)
        browser_navigate_url(url)

def browser_read_docs():
    """Open a documentation page, read it gently, close it."""
    url = random.choice(DOC_URLS)
    browser_navigate_url(url, page_type='docs')

def do_browser_activity():
    """
    Full browser activity session:
    1. Focus browser
    2. Do GitHub or docs activity for 1-2 minutes
    3. Return to VS Code
    """
    log("🌐 Starting browser session...")

    # Switch to browser
    if not focus_browser():
        log("⚠️ Could not focus browser, skipping")
        return

    time.sleep(0.5)

    # Decide what to do in browser
    activity_type = random.choices(
        ['github', 'docs'],
        weights=[70, 30],  # 70% GitHub, 30% docs
        k=1
    )[0]

    # Calculate how long to stay in browser
    stay_duration = random.uniform(BROWSER_STAY_MIN, BROWSER_STAY_MAX)
    end_browser = time.time() + stay_duration

    log(f"🌐 Browser activity: {activity_type} for ~{stay_duration:.0f}s")

    # Do multiple activities within our stay duration
    while time.time() < end_browser and not state.is_paused and not state.should_stop:
        try:
            if activity_type == 'github':
                browser_review_github()
            else:
                browser_read_docs()

            # Small pause between activities within the session
            remaining = end_browser - time.time()
            if remaining > 5:
                time.sleep(random.uniform(2.0, 5.0))
            else:
                break
        except Exception as e:
            log(f"Browser activity error: {e}")
            break

    # Return to VS Code
    time.sleep(random.uniform(0.3, 0.8))
    focus_vscode()
    time.sleep(0.3)

    # Re-focus on editor pane
    pyautogui.hotkey('ctrl', random.choice(['1', '2']))
    state.keyboard_count += 2
    time.sleep(0.3)

    log("🌐 Browser session done, back to VS Code")

def maybe_browser_activity():
    """Check if it's time for browser activity."""
    now = datetime.now()

    if state.last_browser_activity is None:
        state.last_browser_activity = now
        return

    elapsed = (now - state.last_browser_activity).total_seconds()
    trigger = random.randint(BROWSER_MIN_INTERVAL, BROWSER_MAX_INTERVAL)

    if elapsed >= trigger:
        try:
            do_browser_activity()
        except Exception as e:
            log(f"Browser error: {e}")
        finally:
            state.last_browser_activity = datetime.now()

# ============================================================================
# KEYBOARD LISTENER
# ============================================================================

# Track held modifier keys for combo detection
_held_keys = set()

def _do_toggle():
    """Toggle automation on/off."""
    with state.lock:
        state.is_paused = not state.is_paused
        status = "⏸️  PAUSED" if state.is_paused else "▶️  ACTIVE"
        print(f"\n{'='*60}")
        print(f"  Status: {status}")
        if not state.is_paused:
            print(f"  Automation RUNNING")
            print(f"  Scroll Lock / F9 / Ctrl+Shift+X to pause | Mouse→corner to stop")
        else:
            print(f"  Automation PAUSED")
            print(f"  Scroll Lock / F9 / Ctrl+Shift+X to resume")
        print(f"{'='*60}\n")

def on_key_press(key):
    _held_keys.add(key)
    # Single key: Scroll Lock
    if key == TOGGLE_KEY:
        _do_toggle()
    # Combo: Ctrl + Shift + X
    elif hasattr(key, 'char') and key.char and key.char.lower() == 'x':
        if (keyboard.Key.ctrl_l in _held_keys or keyboard.Key.ctrl_r in _held_keys) and \
           (keyboard.Key.shift_l in _held_keys or keyboard.Key.shift_r in _held_keys):
            _do_toggle()
    # Single key: F9 (Easy for Mac keyboards)
    elif key == keyboard.Key.f9:
        _do_toggle()

def on_key_release(key):
    _held_keys.discard(key)

def start_keyboard_listener():
    listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    listener.daemon = True
    listener.start()
    return listener

# ============================================================================
# MAIN LOOP
# ============================================================================

def automation_loop():
    log("Automation ready. Press Scroll Lock (or Ctrl+F8) to start.")

    state.current_project_files = scan_project_files()
    log(f"Found {len(state.current_project_files)} code files")

    if state.current_project_files:
        state.current_file_line_count = get_file_line_count(state.current_project_files[0])

    while not state.should_stop:
        if state.end_time and datetime.now() >= state.end_time:
            log("⏰ Time limit reached!")
            break

        if state.is_paused:
            time.sleep(0.3)
            continue

        try:
            if is_new_minute():
                reset_minute_targets()

            # Periodic special activities
            maybe_switch_file()
            maybe_terminal_activity()
            maybe_browser_activity()

            # Regular keyboard/mouse activity
            remaining_kb = state.target_keyboard - state.keyboard_count
            remaining_mouse = state.target_mouse - state.mouse_count
            remaining_time = get_remaining_time_in_minute()

            if remaining_kb > 0 or remaining_mouse > 0:
                do_kb = should_do_keyboard()
                do_m = should_do_mouse()

                if do_kb and do_m:
                    if random.random() < 0.6:
                        perform_keyboard_action()
                    else:
                        perform_mouse_action()
                elif do_kb:
                    perform_keyboard_action()
                elif do_m:
                    perform_mouse_action()

                total_remaining = remaining_kb + remaining_mouse
                if remaining_time > 0 and total_remaining > 0:
                    ideal = remaining_time / total_remaining
                    delay = random.uniform(
                        max(0.1, ideal * 0.5),
                        min(2.0, ideal * 1.5)
                    )
                else:
                    delay = random.uniform(0.1, 0.5)
                time.sleep(delay)
            else:
                if random.random() < 0.1:
                    if random.random() < 0.5:
                        perform_keyboard_action()
                    else:
                        perform_mouse_action()
                time.sleep(random.uniform(1.0, 3.0))

            if random.random() < 0.02:
                log("Status", show_counts=True)

        except pyautogui.FailSafeException:
            log("🛑 FAIL-SAFE! Stopping...")
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(0.5)

    log("Automation stopped.")

# ============================================================================
# USER INTERFACE
# ============================================================================

def parse_duration(s: str) -> int:
    s = s.lower().strip()
    if s.isdigit():
        return int(s) * 60
    total = 0
    if 'h' in s:
        parts = s.split('h')
        total += int(''.join(filter(str.isdigit, parts[0])) or 0) * 3600
        s = parts[1] if len(parts) > 1 else ''
    if 'm' in s or s:
        d = ''.join(filter(str.isdigit, s))
        if d:
            total += int(d) * 60
    return total if total > 0 else 3600

def format_duration(s: int) -> str:
    h, m = s // 3600, (s % 3600) // 60
    return f"{h}h {m}m" if h > 0 else f"{m}m"

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║          🚀 UPWORK ACTIVITY AUTOMATION v2.3 🚀                    ║
╠═══════════════════════════════════════════════════════════════════╣
║  CONTROLS:                                                        ║
║    • Scroll Lock / F9 / Ctrl+Shift+X  Toggle ON/OFF               ║
║    • Mouse → Corner     Emergency stop                            ║
║    • Ctrl+C             Exit                                      ║
║                                                                   ║
║  ACTIVITY (per minute):                                           ║
║    • Keyboard: {:3d} - {:3d}    • Mouse: {:3d} - {:3d}                     ║
║                                                                   ║
║  FEATURES:                                                        ║
║    • VS Code file switching (~10 min)                             ║
║    • Terminal commands (10-15 min)                                ║
║    • Browser: GitHub PRs, code, docs (8-12 min)                  ║
║    • Dual editor pane support                                     ║
║    • Working directory cache                                      ║
╚═══════════════════════════════════════════════════════════════════╝
    """.format(
        MIN_KEYBOARD_PER_MINUTE, MAX_KEYBOARD_PER_MINUTE,
        MIN_MOUSE_PER_MINUTE, MAX_MOUSE_PER_MINUTE
    ))

def main():
    print_banner()

    # Duration
    print("📋 How long? (30 = minutes, 2h, 1h30m, Enter = unlimited)")
    try:
        d = input("\n⏱️  Duration: ").strip()
        if d == '' or d == '0':
            state.end_time = None
            print("\n✅ Running indefinitely.")
        else:
            secs = parse_duration(d)
            state.end_time = datetime.now() + timedelta(seconds=secs)
            print(f"\n✅ Running for {format_duration(secs)} (until {state.end_time.strftime('%H:%M:%S')})")
    except KeyboardInterrupt:
        print("\n👋 Cancelled.")
        sys.exit(0)

    # Directory
    last_dir = get_last_directory()
    current_dir = os.getcwd()
    print(f"\n📁 Current:   {current_dir}")
    if last_dir != current_dir and os.path.exists(last_dir):
        print(f"   Last used: {last_dir}")
        print("   Enter = last used | '.' = current | or type path")
        default = "last"
    else:
        print("   Enter = current | or type path")
        default = "current"

    d = input(f"\n📂 Directory: ").strip()
    if d == '':
        target = last_dir if default == "last" else current_dir
    elif d == '.':
        target = current_dir
    else:
        target = d
    try:
        os.chdir(target)
        save_last_directory(os.getcwd())
        print(f"   Using: {os.getcwd()}")
    except Exception as e:
        print(f"   Error: {e}, using {os.getcwd()}")

    # Verify browser
    print("\n🌐 Checking for browser window...")
    if find_window('Zen') or find_window('Mozilla') or find_window('brain-battle'):
        print("   ✅ Zen Browser detected")
    else:
        print("   ⚠️  Browser not detected. Make sure Zen Browser is open with GitHub.")
        print("   Browser features will be skipped if window is not found.")

    # Start
    start_keyboard_listener()
    print("\n" + "="*60)
    print("  🎮 READY! Press Scroll Lock (or F9 / Ctrl+Shift+X) to START")
    print("="*60 + "\n")

    try:
        automation_loop()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped.")
    finally:
        state.should_stop = True
        print("\n🏁 Done.")

if __name__ == "__main__":
    main()
