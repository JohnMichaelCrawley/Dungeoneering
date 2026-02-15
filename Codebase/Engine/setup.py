"""
Name: Setup
Filename: setup.py
Date Created: 23rd Jan 2026
Description:

This file helps setup a new game for the player to start a new 
experience in the game

"""
import os
from Player.Player import Player
from jsonLoader import loadPlayerClasses
from Engine.mapSizeConfig import MAPSIZES
from Engine.ui import panel 
classMenu = {"1": "human", "2": "warrior", "3": "mage", "4": "ranger" }
sizeKeys = list(MAPSIZES.keys())
# function confirm options
def confirm (prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type yes/y or no/n")
# function Setup a new game
def setupNewGame(self):   
        PLAYERCLASSES = loadPlayerClasses() 
        # Step 1: Setup player name
        # Player's name setup
        while True:
            # Player's setup
            # Player's name
            panel("Player setup", ["Enter your character's name:"])
            name = input("> ").strip()[:50]
            if not name:
                print("Name cannot be empty")
                continue
            if confirm(f"Use the name '{name}'? (yes/no):"):
                break    
        print("\n")
        # Step 2: Setup player's class
        # Class setup
        panel("Player setup: Select your class",[
            "[1] Human - nothing special",
            "[2] Warrior - Strong, resilient",
            "[3] Mage - Weilder of arcane powers",
            "[4] Ranger - Silent & deadly"])
        while True:
            choice = input("> ").strip()
            if choice not in classMenu:
                print("Invalid class choice. Choose class in 1-4")
                continue
            key = classMenu[choice]
            if key == "human":
             if not confirm("[WARNING]: Human is the hardest class. Are you sure? (yes/no):"):
                continue
            if confirm(f"Use {key.title()} as your class? (yes/no):"):
                break
        self.player = Player(name, PLAYERCLASSES[key])   
        print("\n")
        # Step 3: Setup dungeon size
        panel("Dungeon: Choose dungeon size", [f"[{i+1}] {size.title()}" for i, size in enumerate(sizeKeys)])
        keys = list(MAPSIZES.keys())
        while True:
            choice = input("> ").strip()
            if not choice.isdigit():
                print("Invalid map size!. Enter a valid map size value")
                continue
            number = int(choice)    
            if not (1 <= number <=  len(sizeKeys)):
                print("Invalid map size choice")
                continue
            selected = sizeKeys[number - 1]
            if confirm(f"Use {selected.title()} as the dungeon size? (yes/no):"):
                self.mapSize = MAPSIZES[selected]
                break
            print()  
        print(f"Selected map size: {selected.title()} {self.mapSize}x")   
        print("\n") 
        self.createDungeon()
        print(f"\nWelcome {self.player.name} the {self.player.playerClass}")
        print("You have entered the dungeon, you must clear the dungeon of all enemies..")   
# Restart game
def restartGame(self):
    clearScreenOutput(self)
    self.player = None
    self.dungeon = {}
    self.setupNewGame()
# Game over menu, display when game is finished or player died
def gameOverMenu(self):
    panel("Game over", ["What would you like to do?", "", "[1] start new game?", "[2] Quit game"])
    while True:
        choice = input("> ").strip()
        match choice:
            case "1":
                self.restartGame()
                return
            case "2":
                print("Thank you for playing")
                exit()
            case _:
                print("Invalid selection")
# clear previous outputs on the screen, keeping it clean         
def clearScreenOutput(self):
    os.system("cls" if os.name == "nt" else "clear")