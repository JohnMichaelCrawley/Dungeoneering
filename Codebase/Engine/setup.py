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


PANELWIDTH = 70
classMenu = {"1": "human", "2": "warrior", "3": "mage", "4": "ranger" }
sizeKeys = list(MAPSIZES.keys())
# Panel title
def titlePanel(text):
    print("#" * PANELWIDTH)
    print(f"| {text.ljust(PANELWIDTH - 4)} |")
    print("-" * PANELWIDTH)
# Option list
def optionsPanel(optionsList):
    for option in optionsList:
        print(f"| {option.ljust(PANELWIDTH -4)} |")
    print("#" * PANELWIDTH)
  # Setup a new game
def setupNewGame(self):   
        PLAYERCLASSES = loadPlayerClasses() 
        # Step 1: Setup player name
        # Player's name setup
        while True:
            # Player's setup
            # Player's name
            titlePanel("Player setup: Enter your character's name:")
            name = input("> ").strip()[:50]
            confirm = input(f"Use the name {name}? (yes/no):").lower()
            if confirm == "yes" or confirm == "y":
                break
        print("\n")
        # Step 2: Setup player's class
        # Class setup
        titlePanel("Player setup: Select your class:")
        optionsPanel([
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
                confirm = input(
                    "[Warning]: Human is the hardest class. Are you sure? (yes/no): "
                ).lower()
                if confirm != "yes":
                    continue              
            # Confirm final selection
            confirm = input(f"Use {key.title()} as your class? (yes/no):").lower()
            if confirm == "yes" or confirm == "y":
                break
            break
        self.player = Player(name, PLAYERCLASSES[key])   
        print("\n")
        # Step 3: Setup dungeon size
        titlePanel("Dungeon: Choose dungeon size:")
        optionsPanel([
            f"[{i+1}] {size.title()}" for i, size in enumerate(sizeKeys)
        ])
        keys = list(MAPSIZES.keys())
        while True:
            choice = input("> ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(keys):
                selected = keys[int(choice) - 1]
                self.mapSize = MAPSIZES[selected]
                break
            print("Invalid map size!")
            
            # Confirm final selection
            confirm = input(f"Use {choice} as the dungeon size? (yes/no):").lower()
            if confirm == "yes" or confirm == "y":
                break
            break
        print(f"Selected map size: {selected.title()} {self.mapSize}x")   
        print("\n") 
        self.createDungeon()
        print(f"\nWelcome {self.player.name} the {self.player.playerClass}")
        print("You have entered the dungeon, you must clear the dungeon of all enemies..")   
# clear previous outputs on the screen, keeping it clean         
def clearScreenOutput(self):
    os.system("cls" if os.name == "nt" else "clear")