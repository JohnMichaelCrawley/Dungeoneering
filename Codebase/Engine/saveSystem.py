"""
Name: Save System 
Filename: savesystem.py
Date Created: 23rd Jan 2026
Description:

This file handles saving the game for the player
and check for save files 

"""

import json 
import os

SAVEFILE = "savefile.json"
# Save game
def save(self):
    dungeonData = {}
    for (x, y), room in self.dungeon.items():
        dungeonData[f"{x}, {y}"] = {
            "visited": room.visited,
            "boss": room.boss,
            "locked": getattr(room, "locked", False),
            "items": [item.name for item in room.items]
        }
    data = {
        "player": self.player.toDict(),
        "dungeon": dungeonData
    }
    with open(SAVEFILE, "w") as f:
        json.dump(data, f, indent=2)

# check for save file 
def checkForSaveFile(self):
    if not os.path.exists(SAVEFILE):
        self.setupNewGame()
        return False
    print("Save file found!")
    print("[1] Continue")
    print("[2] New Game")
    print("[3] Delete save file")
    while True:
        choice = input("> ").strip()   
        if choice == "1":
            if self.load():
                print(f"Welcome back, {self.player.name} the {self.player.playerClass}")
                return True
            else:
                print("Failed to load the save file")
                return False
        elif choice == "2":
            os.remove(SAVEFILE)
            print("Starting a new game")
            self.setupNewGame();
            return False
        elif choice == "3":
                confirm = input("[Warning]: All progress will be removed. Are you sure? (yes/no): ").lower()
                if confirm == "yes":
                    os.remove(SAVEFILE)
                    self.setupNewGame();
        else:
            print("Invalid choice - enter 1 or 3")   