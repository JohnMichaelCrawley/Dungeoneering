"""
Name: Actions
Filename: actions.py
Date Created: 23rd Jan 2026
Description:
This file handles the commmand actions the player
uses throughout the game like look in the current room,
eating food or driking potions
"""


"""
    lines = [
        "---",
        "[1] - Continue",
        "[2] - New Game",
        "[3] - Delete save file"
    ]
    panel("Save File Found:", lines)
"""
from Engine.ui import panel
# function look 
def look(self):
    lines = []
    room = self.dungeon[self.player.pos]
    lines.append("---")
    if room.enemies:
        lines.append("Enemies in this room:")
        for i, enemy in enumerate(room.enemies, 1):
            status = f"{enemy.hp}/{enemy.maxHP}"
            lines.append(f"[{i}] {enemy.name} (Level {enemy.level}) HP: {status}")
            lines.append("---") 
    else:
        lines.append("No enemies in the room") 
        lines.append("---") 
    if room.items:
        lines.append("Items:")
        for item in room.items:
            lines.append(f"- {item.name}")
    if room.boss:  
        lines.append("You feel a powerful energy")  
        lines.append("---")   
    panel(f"Current Room: Room: {self.player.pos}", lines)    
# function take <item> 
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
# function drop <item>
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
# # DRY function - consume item for player
def consumeItemForPlayer(self, itemName, requiredType):
    itemName = itemName.lower()
    verb = "ate" if requiredType == "food" else "drank"
    for item in self.player.inventory:
        if item.name.lower() == itemName: 
            if (requiredType == "potion" and item.type not in ["potion", "consumable"]) or (requiredType == "food" and item.type not in ["food", "consumable"]):
                print(f"You cannot {verb} {itemName}")
                return    
            # Apply healing
            if hasattr(item, "heal") and item.heal:
                self.player.hp = min(self.player.maxHP, self.player.hp + item.heal)           
            # apply potion 
            if hasattr(item, "xp") and item.xp:
                self.player.gainXP(item.xp)
            self.player.inventory.remove(item)     
            print(f"You {verb} {item.name}")
            return 
    print(f"You do not have {itemName} in your inventory")
# function eat <item>
def eat(self, foodName):
    self.consumeItemForPlayer(foodName, "food") 
# function drink <potion>
def drink(self, potionName):
    self.consumeItemForPlayer(potionName, "potion") 
# function equip <weapon>
def equip(self, itemName):
    def normalise(text):
        return str(text).strip().lower().replace("’", "'")
    target = normalise(itemName)
    if self.player.weapon and normalise(self.player.weapon.name) == target:
        print(f"You already have {self.player.weapon.name} equipped!")
        return
    for item in self.player.inventory:
        if normalise(item.name) != target:
            continue
        if item.type.lower() != "weapon":
            print(f"{item.name} cannot be equipped")
            return
        playerClass = normalise(self.player.playerClass)
        itemClass   = normalise(item.playerClass or "")
        if itemClass and playerClass != itemClass:
            print(f"You cannot equip {item.name} as {self.player.playerClass}")
            return
        self.player.weapon = item
        print(f"You equipped {item.name}")
        return
    print(f"You do not have {itemName} in your inventory")