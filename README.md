# Claude Code — Status Line + Chime Hook

A custom status line for Claude Code (Windows) with:
- Green progress bars for context, 5h and 7d rate limits
- Reset time displayed next to each quota
- Chime sound when Claude finishes a response

**Preview:**
```
myproject | Claude Sonnet 4.6 | Ctx: ▬▬▬╌╌╌╌╌╌╌ 30% | 5h: ▬▬╌╌╌╌╌╌╌╌ 18% (reset@14:30) | 7d: ▬╌╌╌╌╌╌╌╌╌ 8% (reset@Mon 04/28 02:00)
```

---

## Requirements

- Windows 10/11
- Python 3 installed (from the Microsoft Store or python.org)
- Claude Code CLI

---

## Installation

### 1. Copy the script

Copy `statusline.py` to your Claude config folder:

```
C:\Users\<YOU>\.claude\statusline.py
```

### 2. Find your Python path

Open a terminal and run:

```bash
where python3
# or
where python
```

Copy the full path (e.g. `C:\Users\<YOU>\AppData\Local\Microsoft\WindowsApps\python3.exe`).

### 3. Edit your Claude settings

Open `C:\Users\<YOU>\.claude\settings.json` (create it if it doesn't exist) and add:

```json
{
  "statusLine": {
    "type": "command",
    "command": "cat | C:/Users/<YOU>/AppData/Local/Microsoft/WindowsApps/python3.exe C:/Users/<YOU>/.claude/statusline.py"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"(New-Object System.Media.SoundPlayer 'C:\\\\Windows\\\\Media\\\\chimes.wav').PlaySync()\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

Replace `<YOU>` with your Windows username, and update the Python path to match what you found in step 2.

### 4. Restart Claude Code

The status line and chime will be active immediately.

---

## Customization

Open `statusline.py` and change these two lines at the top:

```python
BAR_WIDTH = 10   # width of each progress bar in characters
BAR_STYLE = 5    # see styles below
```

### Bar styles

| Value | Preview      |
|-------|-------------|
| `1`   | `██████░░░░` |
| `2`   | `▓▓▓▒▒░░░░` gradient |
| `3`   | `●●●●●○○○○○` |
| `4`   | `▶▶▶▶▶·····` |
| `5`   | `▬▬▬▬▬╌╌╌╌╌` (default) |

The filled portion is always displayed in **green**.

### Change the chime sound

Replace `chimes.wav` in the hook command with any `.wav` file path:

```
C:\\Windows\\Media\\notify.wav
C:\\Windows\\Media\\Ring01.wav
```

---

## Troubleshooting

**Status line shows nothing / shows "Claude Code"**
- Make sure Python can be found at the path in `settings.json`
- Test manually: `echo '{}' | python3 C:/Users/<YOU>/.claude/statusline.py`

**No sound on Stop**
- Test manually: `powershell.exe -Command "(New-Object System.Media.SoundPlayer 'C:\Windows\Media\chimes.wav').PlaySync()"`
- Make sure your system volume is not muted
