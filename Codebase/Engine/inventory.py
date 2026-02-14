"""
Name: Inventory
Filename: inventory.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the player's iventory, what items the 
player is currently holding

"""

PANELWIDTH = 70
# Inventory - display items in inventory and display duplicates
def inventory(self):
    print("\n")
    print("#" * PANELWIDTH)
    print(f"| {'Inventory:'.ljust(PANELWIDTH - 4)} |")
    print("-" * PANELWIDTH)
    
    # display player weapon
    if self.player.weapon:
        weaponText = f"Equipped Weapon: {self.player.weapon.name}"
        print(f"| {weaponText.ljust(PANELWIDTH -4 )} |")
        print("-" * PANELWIDTH)
    if not self.player.inventory:
        print(f"| {'You do not currently have anything in your inventory.'.ljust(PANELWIDTH - 4)} |")
        print("#" * PANELWIDTH)
        print()
        return
    # show Items
    print(f"| {'Items:'.ljust(PANELWIDTH - 4)} |")
    print("-" * PANELWIDTH)
    # count duplicate items in inventory
    itemCounts = {}
    for item in self.player.inventory:
        # Skip equipped weapons 
        if self.player.weapon and item is self.player.weapon:
            continue
        itemCounts[item.name] = itemCounts.get(item.name, 0) + 1
    if not itemCounts:
        print(f"| {'You do not currently have anything in your inventory'.ljust(PANELWIDTH - 4)} |")
       
    # print stacked items
    for itemName, count in itemCounts.items():
        if count > 1:
            line = f"- {itemName} (x{count})"
        else:
            line = f"- {itemName}"
        print(f"| {line.ljust(PANELWIDTH - 4)} |")
    print("#" * PANELWIDTH)
    print("\n")
