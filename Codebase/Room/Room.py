"""
Name: Room
Filename: room.py
Date Created: 21 Jan 2026
Description:
This file creates each room in the dungeon setting the enemies, items etc 
within this room in the dungeon
"""
class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.visited = False
        self.items = []
        self.enemies = []
        self.boss = False
        self.locked = False

