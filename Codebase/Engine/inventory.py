"""
Name: Inventory
Filename: inventory.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the player's iventory, what items the 
player is currently holding

"""
def inventory(self):
    print("Inventory:")
    for inventory in self.player.inventory:
        print(f"- {inventory.name}")
    if not self.player.inventory:
        print("You don't currently have anything in your inventory.")
