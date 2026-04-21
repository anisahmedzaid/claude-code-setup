import json, sys, os, datetime
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# ── Config ────────────────────────────────────────────────────────────────────
BAR_WIDTH = 10
BAR_STYLE = 5  # 1=█░  2=▓▒░ gradient  3=●○  4=▶·  5=▬╌ (default)
# ─────────────────────────────────────────────────────────────────────────────

GREEN = "\033[32m"
RESET = "\033[0m"

STYLES = {
    1: ("█", "░"),
    3: ("●", "○"),
    4: ("▶", "·"),
    5: ("▬", "╌"),
}

def make_bar(pct, width=BAR_WIDTH, style=BAR_STYLE):
    filled = max(0, min(width, round(float(pct) / 100.0 * width)))
    empty = width - filled
    if style == 2:
        if filled == 0:
            bar_filled = ""
        elif filled == 1:
            bar_filled = "▒"
        else:
            bar_filled = "▓" * (filled - 1) + "▒"
        return GREEN + bar_filled + RESET + "░" * empty
    fc, ec = STYLES.get(style, STYLES[1])
    return GREEN + fc * filled + RESET + ec * empty

def fmt_reset_time(epoch):
    if not epoch:
        return ""
    try:
        return datetime.datetime.fromtimestamp(int(epoch)).strftime("%H:%M")
    except Exception:
        return ""

def fmt_reset_day(epoch):
    if not epoch:
        return ""
    try:
        dt = datetime.datetime.fromtimestamp(int(epoch))
        return dt.strftime("%a %m/%d %H:%M")
    except Exception:
        return ""

try:
    data = json.load(sys.stdin)
except Exception:
    print("Claude Code", end="")
    sys.exit(0)

try:
    parts = []

    workspace = data.get("workspace") or {}
    cwd = workspace.get("current_dir") or data.get("cwd", "")
    if cwd:
        parts.append(os.path.basename(cwd) or cwd)

    model_info = data.get("model") or {}
    model = model_info.get("display_name", "")
    if model:
        parts.append(model)

    ctx_window = data.get("context_window") or {}
    ctx = ctx_window.get("used_percentage")
    if ctx is not None:
        parts.append("Ctx: %s %.0f%%" % (make_bar(ctx), ctx))

    rate_limits = data.get("rate_limits") or {}
    five_h_data = rate_limits.get("five_hour")
    seven_d_data = rate_limits.get("seven_day")

    five_h = five_h_data.get("used_percentage") if five_h_data else None
    five_h_reset = fmt_reset_time(five_h_data.get("resets_at")) if five_h_data else ""

    seven_d = seven_d_data.get("used_percentage") if seven_d_data else None
    seven_d_reset = fmt_reset_day(seven_d_data.get("resets_at")) if seven_d_data else ""

    if five_h is not None:
        reset_str = (" (reset@%s)" % five_h_reset) if five_h_reset else ""
        parts.append("5h: %s %.0f%%%s" % (make_bar(five_h), five_h, reset_str))
    if seven_d is not None:
        reset_str = (" (reset@%s)" % seven_d_reset) if seven_d_reset else ""
        parts.append("7d: %s %.0f%%%s" % (make_bar(seven_d), seven_d, reset_str))

    if not parts:
        print("Claude Code", end="")
    else:
        print(" | ".join(parts), end="")

except Exception:
    print("Claude Code", end="")
