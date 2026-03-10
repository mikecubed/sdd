"""Agent CLI binary detection for sdd init."""

import shutil


def detect_claude() -> bool:
    """Return True if the claude CLI binary is available in PATH."""
    return shutil.which("claude") is not None


def detect_copilot() -> bool:
    """Return True if the copilot CLI binary is available in PATH."""
    return shutil.which("copilot") is not None
