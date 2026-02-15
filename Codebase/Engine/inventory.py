"""
Name: Inventory
Filename: inventory.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the player's iventory, what items the 
player is currently holding

"""
from Engine.ui import panel
# Inventory - display items in inventory and display duplicates
def inventory(self):
    lines = []
    # equipped weapons
    if self.player.weapon:
        lines.append(f"Equipped Weapon: {self.player.weapon.name}")
        lines.append("")
    # no items 
    if not self.player.inventory:
        lines.append("You do not currently have anything in your inventory")
        panel("Inventory", lines)
        return
    # count duplicates 
    itemCounts = {}
    for item in self.player.inventory:
        if self.player.weapon and item is self.player.weapon:
            continue
        itemCounts[item.name] = itemCounts.get(item.name, 0) + 1
    if not itemCounts:
        lines.append("You do not currently have anything in your inventory")
        panel("Inventory", lines)
        return
    lines.append("Items:")
    lines.append("")
    for itemName, count in itemCounts.items():
        if count > 1:
            lines.append(f"- {itemName} (x{count})")
        else:
            lines.append(f"- {itemName}")
    panel("Inventory", lines)
        
