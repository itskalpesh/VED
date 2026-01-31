"""
VED Router — single entry for decision making.
Uses intent_engine → permission check → ved_os or planner/LLM.

RULE (LOCKED):
- When opening/closing apps, files, or folders:
  → Respond ONLY with: "Opening <name>" / "Closed <name>"
- No explanations, no debug-style text for these actions.
"""

from brain.intent_engine import classify
from brain.permissions import can_run_os_action
from kernel.safety import safe
from ai.hybrid_llm import think
from config.config import DEBUG

# Default mode: "safe" = read-only; "action" = allow OS control
PERMISSION_MODE = "action"


def explainable(action: str, why: str, tool: str, result: str) -> str:
    """Explainable response (used only for non-open actions if needed)."""
    return f"[Action] {action}\n[Why] {why}\n[Tool] {tool}\n[Result] {result}"


def _run_os_action(detail: str, text: str, confirmed_danger: bool) -> str | None:
    """Run OS actions via ved_os and return user-facing response."""
    try:
        import ved_os
    except ImportError:
        if DEBUG:
            print("[ROUTER] ved_os not found; build os_control and add to path.")
        return None

    allowed, reason = can_run_os_action(PERMISSION_MODE, detail, confirmed_danger)
    if not allowed:
        return "Action not allowed."

    text_l = text.strip().lower()

    try:
        # ─────────────────────────────
        # OPEN SOFTWARE
        # ─────────────────────────────
        if detail == "open_software":
            for prefix in ["open ", "launch ", "start ", "run "]:
                if prefix in text_l:
                    app = text_l.split(prefix, 1)[-1].strip()
                    if app and ved_os.open_software(app):
                        return f"Opening {app}"
                    break

        # ─────────────────────────────
        # CLOSE SOFTWARE
        # ─────────────────────────────
        elif detail == "close_software":
            for prefix in ["close ", "quit ", "exit ", "kill ", "stop "]:
                if prefix in text_l:
                    app = text_l.split(prefix, 1)[-1].strip()
                    if app and ved_os.close_software(app):
                        return f"Closed {app}"
                    break

        # ─────────────────────────────
        # OPEN FILE
        # ─────────────────────────────
        elif detail == "open_file":
            if "open file" in text_l:
                idx = text_l.find("open file")
                path = text.strip()[idx + 9:].strip()
                if path and ved_os.open_file(path):
                    name = path.split("\\")[-1].split("/")[-1]
                    return f"Opening {name}"

        # ─────────────────────────────
        # OPEN FOLDER
        # ─────────────────────────────
        elif detail == "open_folder":
            if "open folder" in text_l:
                path = text.strip().split("open folder", 1)[-1].strip()
            elif "open directory" in text_l:
                path = text.strip().split("open directory", 1)[-1].strip()
            else:
                path = text.strip().replace("explore", "").replace("show folder", "").strip()

            if path and ved_os.open_folder(path):
                return f"Opening {path}"

        # ─────────────────────────────
        # OTHER OS ACTIONS (NORMAL TEXT)
        # ─────────────────────────────
        elif detail == "get_running_apps":
            apps = ved_os.get_running_apps()
            return "\n".join(apps[:30]) if apps else "No visible apps."

        elif detail == "find_files":
            parts = text_l.replace("find files", "").replace("find file", "").strip().split()
            directory = "."
            pattern = "*"
            for i, p in enumerate(parts):
                if p in ("in", "under", "from") and i + 1 < len(parts):
                    directory = parts[i + 1]
                    break
            if parts and not parts[0].startswith("in"):
                pattern = parts[0] if "*" in parts[0] else f"*{parts[0]}"
            files = ved_os.find_files(directory, pattern)
            return "\n".join(files[:20]) if files else "No files found."

        elif detail == "request_sleep":
            if ved_os.request_sleep():
                return "System going to sleep."

        elif detail == "lock_workstation":
            if ved_os.lock_workstation():
                return "Workstation locked."

        elif detail == "request_shutdown":
            if ved_os.request_shutdown():
                return "Shutting down."

        elif detail == "request_restart":
            if ved_os.request_restart():
                return "Restarting."

    except Exception as e:
        if DEBUG:
            print(f"[ROUTER] ved_os error: {e}")
        return "Action failed."

    return None


def route(text: str, recall: dict, confirmed_danger: bool = False) -> str:
    """
    Main entry: safety → intent → permission → ved_os or think.
    confirmed_danger: True if user confirmed shutdown/restart.
    """
    if not safe(text):
        if DEBUG:
            print(f"[ROUTER] Blocked unsafe input: {text}")
        return "I'm sorry, but I cannot process that request for safety reasons."

    intent_type, detail = classify(text)

    if intent_type == "os_command" and detail:
        out = _run_os_action(detail, text, confirmed_danger)
        if out is not None:
            return out

    # Non-OS or fallback to LLM
    try:
        return think(text, recall)
    except Exception as e:
        if DEBUG:
            print(f"[ROUTER ERROR] {e}")
        return "I encountered an internal error while processing your request."
