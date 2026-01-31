"""
VED Permission System.
SAFE_MODE = read-only (no OS/file write actions).
ACTION_MODE = controlled execution (OS/file allowed with confirmation for dangerous).
Voice confirmation required for shutdown/restart.
"""

from typing import Literal

PermissionMode = Literal["safe", "action"]

# Dangerous actions that require explicit confirmation (e.g. voice or GUI confirm)
DANGEROUS_OS_ACTIONS = {"request_shutdown", "request_restart"}

# Read-only OS actions (no confirmation needed in ACTION_MODE)
READONLY_OS_ACTIONS = {"get_running_apps", "find_files"}

# Actions that change system state but are not shutdown/restart
STATE_OS_ACTIONS = {"open_software", "close_software", "open_file", "open_folder", "request_sleep", "lock_workstation"}


def can_run_os_action(mode: PermissionMode, action: str, confirmed_danger: bool = False) -> tuple[bool, str]:
    """
    Returns (allowed, reason).
    If action is dangerous (shutdown/restart), confirmed_danger must be True in ACTION_MODE.
    """
    if mode == "safe":
        if action in READONLY_OS_ACTIONS:
            return True, "Read-only action allowed in SAFE_MODE."
        return False, "OS actions are disabled in SAFE_MODE. Switch to ACTION_MODE to allow."

    if mode == "action":
        if action in READONLY_OS_ACTIONS:
            return True, "Read-only action allowed."
        if action in DANGEROUS_OS_ACTIONS:
            if confirmed_danger:
                return True, "Dangerous action confirmed."
            return False, "Shutdown/restart requires voice or GUI confirmation."
        if action in STATE_OS_ACTIONS:
            return True, "Action allowed in ACTION_MODE."
        return False, f"Unknown OS action: {action}."

    return False, "Invalid permission mode."
