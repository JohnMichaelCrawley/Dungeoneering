
"""
Name: Actions
Filename: actions.py
Date Created: 23rd Jan 2026
Description:

This file handles the actions the character has
like eating or drinking or looking in the room

"""


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