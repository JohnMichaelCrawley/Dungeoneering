"""
Name: Player
Filename: player.py
Date Created: 21 Jan 2026
Description:
This file is used to help shape the player, initialise the player, give the ability
to save player's data to dictionary and to allow player to gain XP 
"""
from Player.xpForLevel import xpForLevel
from Item.Item import Item

class Player:
    
    def __init__(self, playerName, playerClass):
        self.name = playerName
        self.playerClass = playerClass["name"]
        self.level = 1
        self.xp = 0
        self.hp = playerClass["hp"]
        self.maxHP = playerClass["hp"]
        self.resource = playerClass["resource"]
        self.maxResource = playerClass["resource"]
        self.resourceName = playerClass["resourceName"]
        self.attacks = playerClass["attacks"]
        self.inventory = []
        self.weapon = None
        self.pos = (0,0)
    # Gain XP 
    def gainXP(self, amount):
        self.xp += amount
        startLevel = self.level 
        while self.xp >= xpForLevel(self.level + 1):
            self.level += 1
            self.maxHP += 5
            self.hp = self.maxHP      
            levelsGained = self.level - startLevel
        if levelsGained == 1:
            print(f"\nCongrats! You reached level {self.level}")
        elif levelsGained > 1:
            print(f"\nYou jumped from level {startLevel} to level {self.level}!")
    # To Dictionary 
    def toDict(self):
        return {
            "name": self.name,
            "playerClass": self.playerClass,
            "level": self.level,
            "xp": self.xp,
            "hp": self.hp,
            "maxHP": self.maxHP,
            "resource": self.resource,
            "maxResource": self.maxResource,
            "resourceName": self.resourceName,
            "pos": list(self.pos),
            # "inventory": [item.name for item in self.inventory],
            "inventory": [item.toDict() for item in self.inventory],
            "weapon": self.weapon.toDict() if self.weapon else None
        } 
    @classmethod
    def fromDict(playerClass, data):
        from Engine.saveSystem import loadItems
        from jsonLoader import loadPlayerClasses
        
        classes = loadPlayerClasses()
        classData = classes[data["playerClass"].lower()]
        
        player = playerClass(
            playerName = data["name"],
            playerClass={
                "name": data["playerClass"],
                "hp": data["hp"],
                "resource": data["maxResource"],
                "resourceName": data["resourceName"],
                "attacks": data.get("attacks") or classData["attacks"]
            }
        )
        player.level = data["level"]
        player.xp = data["xp"]
        player.hp = data["hp"]
        player.maxHP = data["maxHP"]
        player.resource = data["resource"]
        player.maxResource = data["maxResource"]
        if "pos" in data and data["pos"] is not None:
            player.pos = tuple(data["pos"])
        else:
            player.pos = (0, 0)
        
        player.inventory = []
        for itemData in data.get("inventory", []):
            #player.inventory.append(Item(itemData["name"], itemData["type"]))
            player.inventory.append(loadItems(itemData["name"], itemData["type"]))
        player.weapon = None
        
        if data.get("weapon"):
            weaponName = data["weapon"]["name"]
            for item in player.inventory:
                if item.name == weaponName and item.type == "weapon":
                    player.weapon = item
                    player.inventory.remove(item)
                    break
            # player.weapon = Item(data["weapon"]["name"], data["weapon"]["type"])
        else:
            player.weapon = None
        return player
"""     old code   
        for itemName in data.get("inventory", []):
            itemType = "key" if "key" in itemName else "consumable"        
            player.inventory.append(Item(itemName, itemType))
            
        if data.get("weapon"):
            player.weapon = Item(data["weapon"], "weapon")
        else:
            player.weapon = None
        return player"""
        