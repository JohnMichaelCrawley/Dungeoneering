"""
Name: Dungeon
Filename: dungeon.py
Date Created: 23rd Jan 2026
Description:

This file handles the creation of the dungeon
including the enemy spawn and final boss

"""
import random
from Room.Room import Room
from Item.Item import Item
from Enemy.Enemy import Enemy
# function Create the dungeon
def createDungeon(engine):
    size = engine.mapSize
    engine.dungeon = {}
    x, y = 0, 0
    engine.dungeon[(x, y)] = Room(x, y)
    for _ in range(size * size):
        direction = random.choice(["north", "south", "east", "west"])
        match (direction):
            case "north":
                y -= 1
            case "south":
                y += 1
            case "west":
                x -= 1
            case "east":
                x += 1
        if abs(x) <= size // 2 and abs(y) <= size // 2:
            engine.dungeon[(x, y)] = Room(x, y)   
    minX = min(px for px, _ in engine.dungeon)
    minY = min(py for _, py in engine.dungeon)
    normalised = {}
    for (px, py), room in engine.dungeon.items():
        nx, ny = px - minX, py - minY
        room.x, room.y = nx, ny
        normalised[(nx, ny)] = room
    engine.dungeon = normalised
    full = {} # ensure full map
    for yy in range(size):
        for xx in range(size):
            full[(xx, yy)] = engine.dungeon.get((xx, yy), Room(xx, yy))
    engine.dungeon = full
    # normalise player position 
    startPOS = next(iter(engine.dungeon.keys()))
    engine.player.pos = startPOS
    engine.dungeon[startPOS].visited = True
    rooms = list(engine.dungeon.values())    
    # Reset rooms
    for room in rooms:
        room.items.clear()
        room.enemies.clear()
        room.boss = False
        room.locked = False     
    # boss room
    bossRoom = random.choice(rooms[1:])
    bossRoom.boss = True
    bossRoom.locked = True
    bossRoom.enemies = [engine.createFinalBoss()]  
    # Item pools
    foodPool = engine.itemData["food"]
    potionPool = engine.itemData["potions"]
    weaponsPool = engine.itemData["weapons"].copy()
    random.shuffle(weaponsPool)
    for room in rooms:
        if room.boss:
            continue
        # Add Enemies to each room
        if random.random() < 0.7: # 70% chance
            room.enemies = engine.spawnEnemies((1, 5))  
        # Add food
        food = random.choice(foodPool)
        room.items.append(
            Item(
                food["name"],
                "food", 
                heal=food["heal"]
            )
        )
        # Add potions to rooms
        if random.random() < 0.4:
            potion = random.choice(potionPool)
            room.items.append(
                Item(
                    potion["name"],
                    "potion", 
                    heal=potion.get("heal", 0),
                    xp=potion.get("xp", 0)
                )
            )
        # Add weapons to rooms
        if weaponsPool and random.random() < 0.25:
            weapon = weaponsPool.pop()
            room.items.append(
                Item(
                    weapon["name"],
                    "weapon", 
                    power=weapon["power"],
                    playerClass=weapon["playerClass"]
                )
            )
    # key room 
    keyRoom = random.choice([room for room in rooms if not room.boss])
    keyRoom.items.append(Item("Boss Key", "key"))
# function Spawn enemies in rooms   
def spawnEnemies(self, enemySpawnCountRange=(1, 4)):
    enemies = []
    low, high = enemySpawnCountRange
    count = random.randint(low, high)
    for _ in range(count):
        template = random.choice(self.enemyTemplates)
        level = random.randint(1, 5)
        enemies.append(
            Enemy(
                template["name"],
                level,
                template["baseHP"],
                template["baseAttack"],
                template["baseXP"]
            )
        )
    return enemies
# function Create final boss encounter
def createFinalBoss(self):
    template = random.choice(self.enemyTemplates)
    level = random.randint(6, 10)
    return Enemy(
        name=f"Giant {template['name']}",
        level=level,
        baseHP=template["baseHP"] * 2,
        baseAttack=template['baseAttack'] + 3,
        baseXP=template['baseXP'] * 3
    )         