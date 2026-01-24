"""
Name: Combat
Filename: combat.py
Date Created: 23rd Jan 2026
Description:

This file handles the combat system

"""
import random


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