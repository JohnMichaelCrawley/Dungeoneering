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
from Room.Room import Room
from Item.Item import Item
from Enemy.Enemy import Enemy
SAVEFILE = "savefile.json"
# function Load Items
def loadItems(name, itemType):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "..", "data", "Items.json")
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[WARNING] Items.json is not found at {path}")
    for category in data.values():
        for entry in category:
            if entry["name"] == name:
                return Item(
                    name=entry["name"],
                    #(old) itemType=itemType,
                    itemType=entry.get("type", itemType),
                    heal=entry.get("heal", 0),
                    xp=entry.get("xp", 0),
                    power=entry.get("power", 0),
                    playerClass=entry.get("playerClass")
                )
    return Item(name, itemType)
# function Save game
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
        "dungeon": dungeonData,
        "dungeonSize": self.mapSize,
        # save equipped weapon
        "weaponEquipped": (
            {"name": self.player.weapon.name, "type": self.player.weapon.type}
            if self.player.weapon else None
        )
    }
    with open(SAVEFILE, "w") as f:
        json.dump(data, f, indent=2)
# function Load the save file
def load(self):
    from Player.Player import Player
    if not os.path.exists(SAVEFILE):
        return False
    try:
        with open(SAVEFILE, "r") as f:
            data = json.load(f)    
    except json.JSONDecodeError:
        print("Save file is corrupted. Starting new game")
        return False
    # restore player
    self.player = Player.fromDict(data["player"])
    # Restore equipped weapon
    equippedWeapon = data.get("weaponEquipped")
    if equippedWeapon:
        weapon = loadItems(equippedWeapon["name"], equippedWeapon["type"])
        self.player.weapon = weapon
        # remove weapon from inventory if duplicates
        self.player.inventory = [
            item for item in self.player.inventory
            if item.name != weapon.name
        ]
    else:
        self.player.weapon = None 
    # Restore dungeon
    self.mapSize = data.get("dungeonSize", "small")
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
            itemType = "key" if "Key" in itemName else "consumable"
            room.items.append(loadItems(itemName, itemType))
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
            savedHP = enemyData.get("hp", enemy.hp)
            enemy.hp = min(savedHP, enemy.maxHP)  
            if hasattr(enemy, "xp"):
                enemy.xp = enemyData.get("xp", enemy.xp)
            if enemy.hp > 0:
                room.enemies.append(enemy)
        self.dungeon[(x, y)] = room
    return True 
# function check for save file 
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
        if choice in ("q", "quit", "exit"):
            print("Quitting game")
            raise SystemExit       
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