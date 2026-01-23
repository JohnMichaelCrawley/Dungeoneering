"""
Name: Player
Filename: player.py
Date Created: 21 Jan 2026
Description:
This file is used to help shape the player, initialise the player, give the ability
to save player's data to dictionary and to allow player to gain XP 
"""
from Player.xpForLevel import xpForLevel

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
        while self.xp >= xpForLevel(self.level + 1):
            self.level += 1;
            self.maxHP += 5;
            self.hp = self.maxHP
            print(f"\nCongrats! You reached {self.level}")
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
            "inventory": [item.name for item in self.inventory],
            "weapon": self.weapon if self.weapon else None
        }
        
    @classmethod
    def fromDict(playerClass, data):
        player = playerClass(
            playerName = data["name"],
            playerClass={
                "name": data["playerClass"],
                "hp": data["hp"],
                "resource": data["maxResource"],
                "resourceName": data["resourceName"],
                "attacks": []
            }
        )
        player.level = data["level"]
        player.xp = data["xp"]
        player.hp = data["hp"]
        player.maxHP = data["maxHP"]
        player.resource = data["resource"]
        player.maxResource = data["maxResource"]
        player.pos = tuple(data["pos"])
        return player