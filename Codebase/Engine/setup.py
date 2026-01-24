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

  # Setup a new game
def setupNewGame(self):   
        PLAYERCLASSES = loadPlayerClasses() 
        # Player's name setup
        while True:
            name = input("Enter your character's name: ").strip()[:50]
            confirm = input(f"Use the name {name}? (yes/no):").lower()
            if confirm == "yes" or confirm == "y":
                break
        
        # Map size selection
        print("\nChoose the dungeon size:")
        for i, size in enumerate(MAPSIZES.keys(), 1):
            print(f"[{i}] {size.title()}")
        keys = list(MAPSIZES.keys())
        
        while True:
            choice = input("> ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(keys):
                selected = keys[int(choice) - 1]
                self.mapSize = MAPSIZES[selected]
                break
            print("Invalid map size!")
        
        print(f"Selected map size: {selected.title()} {self.mapSize}x")
        
        
        print("######################################")
        print("""Choose your class: \n[1] - Human\n[2] - Warrior\n[3] - Mage\n[4] - Ranger""")
        print("######################################")
        classMenu = {"1": "human", "2": "warrior", "3": "mage", "4": "ranger" }
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
            break
        self.player = Player(name, PLAYERCLASSES[key])
        self.createDungeon()
        print(f"\nWelcome {self.player.name} the {self.player.playerClass}")
        print("You have entered the dungeon, you must clear the dungeon of all enemies..")   
     
# clear previous outputs on the screen, keeping it clean         
def clearScreenOutput(self):
    os.system("cls" if os.name == "nt" else "clear")