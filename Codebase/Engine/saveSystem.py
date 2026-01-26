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
from Player.Player import Player
from Room.Room import Room
from Item.Item import Item
from Enemy.Enemy import Enemy

SAVEFILE = "savefile.json"
# Save game
def save(self):
    dungeonData = {}
    for (x, y), room in self.dungeon.items():
        dungeonData[f"{x}, {y}"] = {
            "visited": room.visited,
            "boss": room.boss,
            "locked": getattr(room, "locked", False),
            "items": [item.name for item in room.items],
            "enemies": [
                {
                    "name": enemy.name,
                    "level": enemy.level,
                    "hp": enemy.hp
                }
                for enemy in room.enemies
            ]
        }      
    data = {
        "player": self.player.toDict(),
        "dungeon": dungeonData
    }
    with open(SAVEFILE, "w") as f:
        json.dump(data, f, indent=2)
# Load the save file
def load(self):
    if not os.path.exists(SAVEFILE):
        return False
    with open(SAVEFILE, "r") as f:
        data = json.load(f)    
    # restore data
    self.player = Player.fromDict(data["player"])
    self.dungeon = {}
    # rebuild rooms
    for key, roomData in data["dungeon"].items():
        x, y = map(int, key.split(","))
        room = Room(x, y) 
        room.visited = roomData["visited"]
        room.boss = roomData["boss"]
        room.locked = roomData.get("locked", False) 
        room.items = []
        for itemName in roomData.get("items", []):
            room.items.append(Item(itemName, "key" if "Key" in itemName else "consumable"))
        # re-add enemies
        room.enemies = []
        for enemyData in roomData.get("enemies", []):
            enemy = Enemy(
                enemyData["name"],
                enemyData["level"],
                baseHP=0,
                baseAttack=0,
                baseXP=enemyData.get("xp", 0)
            )
            enemy.hp = enemyData.get("hp", enemy.hp)
            if hasattr(enemy, "xp"):
                enemy.xp = enemyData.get("xp", enemy.xp)
            if enemy.hp > 0:
                room.enemies.append(enemy)
        self.dungeon[(x, y)] = room
    return True 

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
                    return False
        else:
            print("Invalid choice - enter 1 or 3")