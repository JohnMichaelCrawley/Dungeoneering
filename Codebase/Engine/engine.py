"""
Name: Engine
Filename: engine.py
Date Created: 23rd Jan 2026
Description:
This is the main initialiser class for the game engine
"""

import curses
import builtins
import contextlib
from Engine.ui import LOGO, uiRenderHeader, uiGetHeaderHeight
from Engine.setup import setupNewGame, clearScreenOutput
from Engine.saveSystem import save, checkForSaveFile
from Commands.Command import Commands
from jsonLoader import loadEnemiesToGame, loadItemsToGame
from Engine.mapSizeConfig import MAPSIZES
from Engine.dungeon import createDungeon, spawnEnemies, createFinalBoss
from Engine.movement import move
from Engine.combat import attack
from Engine.actions import look, take, drop, eat, drink, equip, consumeItemForPlayer
from Engine.inventory import inventory
from Engine.mapRenderer import map
from Engine.stats import stats
from Engine.help import help


class GameEngine:
    # initialise the game
    def __init__(self):
        # Set up game state, load enemies/items, and bind engine actions
        self.dungeon = {}
        self.player = None
        self.enemyTemplates = list(loadEnemiesToGame()["enemies"])
        self.itemData = loadItemsToGame()
        self.mapSize = MAPSIZES["medium"]
        # Bind engine actions
        self.createDungeon = createDungeon.__get__(self)
        self.move = move.__get__(self)
        self.attack = attack.__get__(self)
        self.look = look.__get__(self)
        self.consumeItemForPlayer = consumeItemForPlayer.__get__(self)
        self.take = take.__get__(self)
        self.drop = drop.__get__(self)
        self.eat = eat.__get__(self)
        self.drink = drink.__get__(self)
        self.equip = equip.__get__(self)
        self.help = help.__get__(self)
        self.inventory = inventory.__get__(self)
        self.map = map.__get__(self)
        self.stats = stats.__get__(self)
        self.save = save.__get__(self)
        self.checkForSaveFile = checkForSaveFile.__get__(self)
        self.setupNewGame = setupNewGame.__get__(self)
        self.clearScreenOutput = clearScreenOutput.__get__(self)
        self.spawnEnemies = spawnEnemies.__get__(self)
        self.createFinalBoss = createFinalBoss.__get__(self)
        self.commands = Commands(self)
        # curses UI state 
        self._stdscr = None
        self._logLines = []
        self._pendingFragment = ""
        self._statusLine = ""
        self._lastPrompt = ""
        self._running = True
    # Title - Start curses UI and launch the game engine
    def title(self):
        curses.wrapper(self._cursesMain)
    # Curses Main - Main curses entry point — sets up UI and runs game loop
    def _cursesMain(self, stdscr):
        self._stdscr = stdscr
        self._setupCurses(stdscr)
        # Title screen (curses)
        self._titleScreen(stdscr)
        # Patch print/input so game logic uses curses UI
        with self._patchedStdio():
            self.checkForSaveFile()
            self.commandLoop()
    # Setup Curses - Configure curses display settings (colors, input mode, redraw)
    def _setupCurses(self, stdscr):
        curses.curs_set(1)
        stdscr.keypad(True)
        stdscr.timeout(50)
        try:
            if curses.has_colors():
                curses.start_color()
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                stdscr.bkgd(" ", curses.color_pair(1))
        except Exception:
            pass

    # Title Screen - Display the intro/title screen before starting gameplay
    def _titleScreen(self, stdscr):
        curses.curs_set(0)
        introText = [
            "Version: [In-Development] | Date released: [] | Last Update: []",
            "",
            "DUNGEONEERING: A text adventure game by John Crawley, built using Python & JSON as a fun project to work on.",
            "",
            "The purpose of this text adventure game is to explore the dungeon, grow stronger by finding items, defeating enemies and then find a key to enter the boss room and defeat it.",
            "",
            "If you require help, enter the command 'help' and it will display a list of commands you can use in this game.",
            "", 
            "- John Crawley © 2026 -",
            "",
            "",
            "Press ENTER to begin your adventure."
        ]
        while True:
            uiRenderHeader(stdscr, LOGO, introText)
            key = stdscr.getch()
            if key == curses.KEY_RESIZE:
                continue
            if key in (10, 13, curses.KEY_ENTER):
                break
        curses.curs_set(1)
        self._logLines.clear()
        self._pendingFragment = ""
        self._statusLine = ""
        self._render(input_text="", prompt="")
    # Command Loop - Main command input loop — reads player commands and executes them
    def commandLoop(self):
        self._lastPrompt = "> "
        self._uiPrint("")
        self._uiPrint("Type 'help' for commands. Resize anytime.")
        self._uiPrint("")
        while self._running:
            cmd = self._uiInput("> ").strip()
            if not cmd:
                continue
            tokens = cmd.split()
            try:
                self.commands.execute(tokens)
            except SystemExit:
                self._running = False
            except Exception as e:
                self._uiPrint(f"[Error] {e}")
    # Patch print() and input() so they render inside curses UI
    @contextlib.contextmanager
    def _patchedStdio(self):
        oldPrint = builtins.print
        oldInput = builtins.input
        builtins.print = self._uiPrint
        builtins.input = self._uiInput
        try:
            yield
        finally:
            builtins.print = oldPrint
            builtins.input = oldInput

    # UI Print - Capture printed output and store it in the log buffer
    def _uiPrint(self, *args, sep=" ", end="\n", **kwargs):
        text = sep.join(str(a) for a in args)
        if self._pendingFragment:
            text = self._pendingFragment + text
            self._pendingFragment = ""
        if end != "\n":
            self._pendingFragment = text
            self._render(input_text="", prompt=self._lastPrompt)
            return
        for line in text.splitlines():
            self._logLines.append(line)
        if len(self._logLines) > 3000:
            self._logLines = self._logLines[-2500:]
        self._render(input_text="", prompt=self._lastPrompt)
    # UI Input - Handle player input inside curses (text editing, enter, navigation)
    def _uiInput(self, prompt=""):
        self._lastPrompt = prompt
        buf = []
        cursor = 0
        while True:
            current = "".join(buf)
            self._render(input_text=current, prompt=prompt, cursor_pos=cursor)
            ch = self._stdscr.getch()
            if ch == -1 or ch == curses.KEY_RESIZE:
                continue
            # ENTER submits input
            if ch in (10, 13, curses.KEY_ENTER):
                self._uiPrint(f"{prompt}{''.join(buf)}")
                return "".join(buf)
            # ESC cancels input
            if ch == 27:
                self._uiPrint(f"{prompt}")
                return ""
            # BACKSPACE deletes character
            if ch in (8, 127, curses.KEY_BACKSPACE):
                if cursor > 0:
                    buf.pop(cursor - 1)
                    cursor -= 1
                continue
            # Cursor movement
            if ch == curses.KEY_LEFT:
                cursor = max(0, cursor - 1)
                continue
            if ch == curses.KEY_RIGHT:
                cursor = min(len(buf), cursor + 1)
                continue
            if ch == curses.KEY_HOME:
                cursor = 0
                continue
            if ch == curses.KEY_END:
                cursor = len(buf)
                continue
            # Delete key
            if ch == curses.KEY_DC:
                if cursor < len(buf):
                    buf.pop(cursor)
                continue
            # Printable text input
            if 32 <= ch <= 126:
                buf.insert(cursor, chr(ch))
                cursor += 1
                continue
    # Render - Render the full curses UI (header, log, and input bar)
    def _render(self, input_text="", prompt="", cursor_pos=None):
        stdscr = self._stdscr
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        if h < 10 or w < 30:
            msg = "Resize window..."
            try:
                stdscr.addstr(max(0, h // 2), max(0, (w - len(msg)) // 2), msg[: max(0, w - 1)])
            except Exception:
                pass
            stdscr.refresh()
            return
        uiRenderHeader(stdscr, LOGO, [])
        headerHeight = uiGetHeaderHeight(LOGO)
        top = min(headerHeight + 1, h - 3)
        bottomInputY = h - 2
        logHeight = max(1, bottomInputY - top)
        visible = self._logLines[-logHeight:]
        y = top
        for line in visible:
            if y >= bottomInputY:
                break
            self._safeAddstr(y, 2, line, w)
            y += 1
        inputLine = f"{prompt}{input_text}"
        self._safeAddstr(bottomInputY, 2, inputLine, w)
        if cursor_pos is not None:
            cursor_x = 2 + len(prompt) + cursor_pos
            cursor_x = max(0, min(w - 1, cursor_x))
            try:
                stdscr.move(bottomInputY, cursor_x)
            except Exception:
                pass
        stdscr.refresh()
    # Safe Add String - Safely write text to screen without crashing on resize
    def _safeAddstr(self, y, x, s, w):
        if y < 0 or x >= w or not s:
            return
        if x < 0:
            s = s[-x:]
            x = 0
        s = s[: max(0, w - x - 1)]
        try:
            self._stdscr.addstr(y, x, s)
        except Exception:
            pass