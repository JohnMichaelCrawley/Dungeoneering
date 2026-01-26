"""
Name: User Interface
Filename: ui.py
Date Created: 23rd Jan 2026
Description:
This file creates the user interface of the terminal to give the
game a more classic text adventure feel. 

This is used in two contexts:
1 - inside curses (e.g: the title screen)
2 - outside curses (ormal print, input or gameloop)


"""
from __future__ import annotations
import curses
import shutil
import textwrap
from typing import Iterable, List, Optional

LOGO = r"""██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗ ███████╗ ███████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗
██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗████╗  ██║ ██╔════╝ ██╔════╝██╔═══██╗██╔══██╗██║████╗  ██║██╔════╝
██║  ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██╔██╗ ██║ █████╗   █████╗  ██║   ██║██████╔╝██║██╔██╗ ██║██║  ███╗
██║  ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║╚██╗██║ ██╔══╝   ██╔══╝  ██║   ██║██╔══██╗██║██║╚██╗██║██║   ██║
██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██║ ╚████║ ███████╗ ███████╗╚██████╔╝██║  ██║██║██║ ╚████║╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚══════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝"""


# terminal Size Fallback
## Return terminal size (cols, rows)
def terminalSizeFallback() -> tuple[int, int]:
    try:
        sz = shutil.get_terminal_size(fallback=(80, 24))
        return sz.columns, sz.lines
    except Exception:
        return 80, 24
# Safe Clip
def safeClip(text: str, width: int) -> str:
    if width <= 0:
        return ""
    return text[:width] if len(text) > width else text
# Safe Add String - Write strings safely, like clip to screen width and sallow curse errors
def _safeAddstr(stdscr: "curses._CursesWindow", y: int, x: int, s: str, attr: int = 0) -> None:
    try:
        h, w = stdscr.getmaxyx()
        if y < 0 or y >= h:
            return
        if x < 0:
            # clip left
            s = s[-x:]
            x = 0
        if x >= w:
            return
        if not s:
            return
        s = safeClip(s, w - x)
        if not s:
            return
        stdscr.addstr(y, x, s, attr)
    except curses.error:
        # Happens when terminal is tiny or mid-resize.
        return
# initalise Black screen - attempt to give the terminal a black background. Return attributes to use for drawing
def _initBlackScreen(stdscr: "curses._CursesWindow") -> int:
    attr = 0
    try:
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            # Use explicit black background when available.
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            attr = curses.color_pair(1)
            stdscr.bkgd(" ", attr)
        else:
            stdscr.bkgd(" ")
    except Exception:
        # Non-fatal.
        attr = 0
    return attr
# UI Get Header Height
def uiGetHeaderHeight(logo: str) -> int:
    visible_lines = [ln for ln in logo.splitlines() if ln.strip()]
    return len(visible_lines) + 2  # top + bottom border only
# Draw Header Line
def _drawHline(stdscr: "curses._CursesWindow", y: int, x: int, width: int, attr: int = 0) -> None:
    if width <= 0:
        return
    _safeAddstr(stdscr, y, x, "-" * width, attr)
# Draw Logo Title With Cropped Text
def drawLogoTitleWithCroppedText(
    stdscr: "curses._CursesWindow",
    start_y: int,
    start_x: int,
    box_width: int,
    logo: str,
    attr: int = 0,
) -> int:
    # Draw logo inside a bordered box. Returns next y position
    _drawHline(stdscr, start_y, start_x, box_width, attr)
    y = start_y + 1
    inner_width = max(0, box_width - 4)
    for raw in logo.splitlines():
        if raw == raw.rstrip():
            if not raw:
                continue
        clipped = safeClip(raw, inner_width)
        line = f"| {clipped.ljust(inner_width)} |"
        _safeAddstr(stdscr, y, start_x, line, attr)
        y += 1
    _drawHline(stdscr, y, start_x, box_width, attr)
    return y + 1
# Draw Text Box
def drawTextBox(
    stdscr: "curses._CursesWindow",
    start_y: int,
    start_x: int,
    box_width: int,
    lines: Iterable[str],
    line_spacing: int = 1,
    attr: int = 0,
) -> int:
    """Draw wrapped text lines inside a bordered box. Returns next y position."""
    _drawHline(stdscr, start_y, start_x, box_width, attr)
    y = start_y + 1
    innerWidth = max(0, box_width - 4)
    for entry in lines:
        wrapped = textwrap.wrap(entry, innerWidth) if innerWidth > 0 else [""]
        wrapped = wrapped or [""]
        for lineText in wrapped:
            line = f"| {lineText.ljust(innerWidth)} |"
            _safeAddstr(stdscr, y, start_x, line, attr)
            y += 1
        for _ in range(max(0, line_spacing)):
            line = f"| {' '.ljust(innerWidth)} |"
            _safeAddstr(stdscr, y, start_x, line, attr)
            y += 1
    _drawHline(stdscr, y, start_x, box_width, attr)
    return y + 1
# UI Render Header
def uiRenderHeader(
    stdscr: "curses._CursesWindow",
    logo: str,
    text_lines: Optional[List[str]] = None,
) -> None:
    # Render the title header. Safe under aggressive resizing
    attr = _initBlackScreen(stdscr)
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    text_lines = text_lines or []
    # If the window is extremely small, show a minimal message.
    if h < 6 or w < 20:
        msg = "Resize the window…"
        _safeAddstr(stdscr, max(0, h // 2), max(0, (w - len(msg)) // 2), safeClip(msg, w), attr)
        stdscr.refresh()
        return
    # Keep a nice big centered box, but never exceed screen width.
    box_width = min(w - 2, max(40, w - 4))
    box_width = max(20, box_width)
    x = max(0, (w - box_width) // 2)
    y = 1
    y = drawLogoTitleWithCroppedText(stdscr, y, x, box_width, logo, attr=attr)
    if text_lines:
        y += 1
        drawTextBox(stdscr, y, x, box_width, text_lines, line_spacing=0, attr=attr)
    stdscr.refresh()
# Print Persistent Header
def printPersistentHeader(extra_lines: Optional[List[str]] = None) -> None:
    # Print a persistent header for the non-curses parts of the gam
    # This is used after the curses title screen exits, when the game returns to
    # plain stdout + `input()` prompts.
    # It clears the screen and prints a bordered logo box that adapts to the
    # current terminal width.
    cols, _rows = terminalSizeFallback()
    # Leave a bit of padding for safety
    box_width = max(20, min(cols - 2, max(60, cols - 4)))
    inner_width = max(0, box_width - 4)
    # ANSI clear screen + home cursor. (Works in most terminals.)
    print("\033[2J\033[H", end="")
    border = "-" * box_width
    print(border)
    for raw in LOGO.splitlines():
        raw = raw.rstrip()
        if not raw:
            continue
        clipped = safeClip(raw, inner_width)
        print(f"| {clipped.ljust(inner_width)} |")
    print(border)
    extra_lines = extra_lines or []
    if extra_lines:
        print()
        print(border)
        for entry in extra_lines:
            wrapped = textwrap.wrap(entry, inner_width) or [""]
            for line in wrapped:
                print(f"| {line.ljust(inner_width)} |")
        print(border)