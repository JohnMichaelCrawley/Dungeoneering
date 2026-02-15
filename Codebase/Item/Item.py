"""
Name: Item
Filename: item.py
Date Created: 21 Jan 2026
Description:
This file creates the model of each item which includes values like
the name of item, type of the item which includes weapon, key or a consumable and 
which player class this is for 
"""
class Item:
    def __init__(self, name, itemType, heal=0, xp=0, power=0, playerClass=None):
        self.name = name
        self.type = itemType # i.e: weapon, consumable, key
        self.heal = heal
        self.xp = xp
        self.power = power
        self.playerClass = playerClass
    # To Dictionary 
    def toDict(self):
        return {
            "name": self.name,
            "type": self.type
        }