"""
Name: Game Engine
Filename: gameengine.py
Date Created: 22 Jan 2026
Description:
This file is core system of the text adventure game where the main functionality
is done like player movement, attacks, load/saves etc
"""
import random
import json 
import os
from Commands.Command import Commands
from Room.Room import Room
from Enemy.Enemy import Enemy
from Item.Item import Item
from Player.Player import Player
from jsonLoader import loadEnemiesToGame, loadPlayerClasses, loadItemsToGame

SAVEFILE = "savefile.json"
MAPSIZE = 5 ## Set to 10

class GameEngine:
    def __init__(self):
        self.dungeon = {}
        self.player = None
        self.commands = Commands(self)
        self.enemyTemplates = list(loadEnemiesToGame()["enemies"])
        self.itemsData = loadItemsToGame()
        self.usedWeapons = set()
        
    def title(self):
               print("""
██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗ ███████╗ ███████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗
██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗████╗  ██║ ██╔════╝ ██╔════╝██╔═══██╗██╔══██╗██║████╗  ██║██╔════╝
██║  ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██╔██╗ ██║ █████╗   █████╗  ██║   ██║██████╔╝██║██╔██╗ ██║██║  ███╗
██║  ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║╚██╗██║ ██╔══╝   ██╔══╝  ██║   ██║██╔══██╗██║██║╚██╗██║██║   ██║
██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██║ ╚████║ ███████╗ ███████╗╚██████╔╝██║  ██║██║██║ ╚████║╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚══════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝

Version: [In-Development] | Date released: [] | Last Update: []

DUNGEONEERING: Text Adventure Game by John Crawley, build using Python & JSON as a fun project to work on

The purpose of this text adventure game is to explore the dungeon, grow stronger by finding items, defeating enemies and 
then find a key to enter the boss room and defeat it.

If you require help, enter the command 'help' and it will display a list of commands you can use in this game


- John Crawley © 2026 - 
""")
    # Create the dungeon
    def createDungeon(self):
        self.dungeon = {}
        x, y = 0, 0
        self.dungeon[(x, y)] = Room(x, y)
        for _ in range(MAPSIZE * MAPSIZE):
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
            if abs(x) <= MAPSIZE // 2 and abs(y) <= MAPSIZE // 2:
                self.dungeon[(x, y)] = Room(x, y)   
        minX = min(px for px, _ in self.dungeon)
        minY = min(py for _, py in self.dungeon)
        normalised = {}
        for (px, py), room in self.dungeon.items():
            nx, ny = px - minX, py - minY
            room.x, room.y = nx, ny
            normalised[(nx, ny)] = room
        self.dungeon = normalised
        ## ensure full map
        full = {}
        for yy in range(MAPSIZE):
            for xx in range(MAPSIZE):
                full[(xx, yy)] = self.dungeon.get((xx, yy), Room(xx, yy))
        self.dungeon = full
        
        # normalise player position 
        startPOS = next(iter(self.dungeon.keys()))
        self.player.pos = startPOS
        self.dungeon[startPOS].visited = True
        
        rooms = list(self.dungeon.values())    
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
        bossRoom.enemies = [self.createFinalBoss()]  
        # Item pools
        foodPool = self.itemsData["food"]
        potionPool = self.itemsData["potions"]
        weaponsPool = self.itemsData["weapons"].copy()
        random.shuffle(weaponsPool)
        
        for room in rooms:
            if room.boss:
                continue
            # Add Enemies to each room
            if random.random() < 0.7: # 70% chance
                room.enemies = self.spawnEnemies((1, 3))  
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
        #startPOS = next(iter(self.dungeon.keys()))
        #self.player.pos = startPOS
        #self.dungeon[startPOS].visited = True  
        
        
        
        
        
        
        
        
        
                
    # Help command to learn about other commannds
    def help(self):
        print("""
Help:
###################
Command list:
    - go (north, south, east, west)
    - look (see what's in the room)
    - attack ('attack' just attacks the first thing in the room, otherwise, 'attack [value]' attacks enemy based on enemy number)
    - iventory / i (check your inventory)
    - eat 
    - drink
    - take (take + item = goes to your inventory)
    - map (check the map and where you are)
    - stats (check the character stats)
    - save (save the game and your progress)
###################""")
    # Move somewhere
    def move(self, direction):
        
        x, y = self.player.pos
        directions = { 
            "north":(0, -1), 
            "south":(0, 1), 
            "west":(-1, 0), 
            "east":(1, 0) 
        }
        dx, dy = directions.get(direction, (0, 0))
        newPOS = (x+dx, y+dy)
        
        if newPOS not in self.dungeon:
           # self.player.pos = newPOS
            #self.dungeon[newPOS].visited = True
            #self.look()
            print("You hit a wall")
            return   
        # locked room check
        room = self.dungeon[newPOS]
        if room.boss and room.locked:
            hasKey = any(item.name == "Boss Key" for item in self.player.inventory)
            if not hasKey:
                print("The door is locked. You need to find the key to enter")
                return
            else:
                print("You unlocked the massive door")
                room.locked = False
        # move player
        self.player.pos = newPOS
        room.visited = True
        self.look()    
    # Spawn enemies in rooms   
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
    # Create final boss encounter
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
    # Look at something 
    def look(self):
        room = self.dungeon[self.player.pos]
        print(f"\n Room {self.player.pos}")  
        if room.enemies:
            print("Enemies in the room:")
            for i, enemy in enumerate(room.enemies, 1):
                status = f"{enemy.hp}/{enemy.maxHP}"
                print(f" [{i}] {enemy.name} (Level {enemy.level}) HP: {status}")
        else:
            print("No enemies in the room")  
        if room.items:
            print("Items:", ", ".join(item.name for item in room.items))
        if room.boss:  
            print("You feel a powerful energy")        
    # Attack enemy    
    def attack(self, index=0):
        room = self.dungeon[self.player.pos]
        if not room.enemies:
            print("Nothing to attack")
            return 
        if index < 0 or index >= len(room.enemies):
            print("Invalid enemy number")
            return       
        enemy = room.enemies[index]           
        damage = random.randint(3, 6)
        if self.player.weapon:
            damage += self.player.weapon.power
        enemy.hp -= damage
        print(f"You hit the {enemy.name} for {damage} damage")
        if enemy.alive():
            self.player.hp -= enemy.attack
            print(f"The {enemy.name} hits you for {enemy.attack} damage")
            print("--------------------------------------------")
            print(f"{enemy.name}'s health is {enemy.hp}")
            print(f"Your health is now at {self.player.hp}")
            print("--------------------------------------------")
            if self.player.hp <= 0:
                print(f"\nYou have been slain by {enemy.name}...") 
                exit()
        else:
            print(f"You defeated {enemy.name}")
            self.player.gainXP(enemy.xp)
            room.enemies.remove(enemy)
            if room.boss:
                print("\nYou have cleared the dungeon!")
                exit()
    # Take item
    def take(self, itemName):
        room = self.dungeon[self.player.pos]
        if not room.items:
            print("There is nothing to take in this room")
            return 
        
        itemName = itemName.lower()
        itemsToTakeFromTheRoom = []
        
        for item in room.items:
                if itemName == "all" or item.name.lower() == itemName:
                    # boss key protection
                    if item.name == "Boss Key" and room.enemies:
                        print("You cannot take the Boss Key while enemies remain")
                        continue
                    
                    itemsToTakeFromTheRoom.append(item)
                    
                    if not itemsToTakeFromTheRoom:
                        print(f"There is no {itemName} here")
                        return
        if not itemsToTakeFromTheRoom:
            print(f"There is no {itemName} here")
            return
        
        for item in itemsToTakeFromTheRoom:
            room.items.remove(item)
            self.player.inventory.append(item)
            print(f"You picked up {item.name}")                 
    # Drop item from inventory
    def drop(self, itemName):
        room = self.dungeon[self.player.pos]
        for item in self.player.inventory[:]:
            if item.name.lower() == itemName.lower():
                self.player.inventory.remove(item)
                room.items.append(item)
                
                if self.player.weapon == item:
                    self.player.weapon = None
                    print(f"You dropped {item.name} and unequipped it")
                else:
                    print(f"You dropped {item.name}")
                return
        print(f"You do not have have {item.name}")    
    # Show player's inventory
    def inventory(self):
        print("Inventory:")
        for inventory in self.player.inventory:
            print(f"- {inventory.name}")
        if not self.player.inventory:
            print("You don't currently have anything in your inventory.")
    # DRY function - consume item for player
    def consumeItemForPlayer(self, itemName, requiredType):
        itemName = itemName.lower()
        verb = "ate" if requiredType == "food" else "drank"
        for item in self.player.inventory:
            if item.name.lower() == itemName: 
                # wrong item type
                if item.type != requiredType:
                    print("You cannot {verb} {item.name}")
                    return       
                # Apply healing
                if item.heal:
                    self.player.hp = min(self.player.maxHP, self.player.hp + item.heal)           
                # apply potion 
                if hasattr(item, "xp") and item.xp:
                    self.player.gainXP(item.xp)
                # remove item from iventory
                self.player.inventory.remove(item)     
                # output final message 
                print(f"You {verb} {item.name}")
                return 
                #print(f"You used {item.name}") 
        print(f"You do not have {itemName} in your inventory")
    # Eat items
    def eat(self, foodName):
        self.consumeItemForPlayer(foodName, "food") 
    # Drink potions
    def drink(self, potionName):
        self.consumeItemForPlayer(potionName, "potion") 
    # Equip item
    def equip(self, itemName):
        for item in self.player.inventory:
            if item.name.lower() == itemName.lower() and item.type == "weapon":
                if item.playerClass != self.player.playerClass:
                    print(f"You cannot equip {item.name} as {self.player.playerClass}")
                    return
                self.player.weapon = item
                print(f"You equipped {item.name}") 
                return 
        print(f"You do not have {itemName}")
    # See dungeon map ▼
    def map(self):
        width = MAPSIZE
        # build the horzintaol grid row dynamically
        horizontal = "+" + "---+" * width
        # frame width based on grid
        framedWidth = len("## " + horizontal + " ##")
        # border line
        border = "#" * framedWidth
        print("\nDungeon Map:")
        # Top border
        print(border+"\n"+border)
        for y in range(width):
            print("## " + horizontal + " ##")
            # Room row
            row = "## |"
            for x in range(width):
                if (x, y) == self.player.pos:
                    row += " ▼ |"
                elif (x, y) in self.dungeon and self.dungeon[(x, y)].visited:
                    row += " x |"
                else:
                    row += "   |"
            row += " ##"
            print(row)
        # bottom grid seperator
        print("## " + horizontal + " ##")
        print(border+"\n"+border)          
                             
    # See player stats  
    def stats(self):
        print("##############################")
        print(f"""{self.player.name} the {self.player.playerClass} \n - Level: {self.player.level}  \n - XP: {self.player.xp} \n - HP: {self.player.hp}/{self.player.maxHP}""")
        print("##############################")
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
    # Load save file
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
            for itemName in roomData.get("items", []):
                room.items.append(Item(itemName, "key" if "Key" in itemName else "consumable"))
            self.dungeon[(x, y)] = room
        return True 
    # Setup a new game
    def setupNewGame(self):   
            PLAYERCLASSES = loadPlayerClasses() 
            name = input("Enter your character's name: ").strip()[:50]
            
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
    # clear previous outputs on the screen, keeping it clean         
    def clearScreenOutput(self):
        os.system("cls" if os.name == "nt" else "clear")