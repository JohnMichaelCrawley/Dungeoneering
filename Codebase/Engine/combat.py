"""
Name: Combat
Filename: combat.py
Date Created: 23rd Jan 2026
Description:

This file handles the combat system
from getting available attacks, choosing attacks
and finally the attack function
"""
import random
from Engine.stats import stats
from Engine.ui import panel
# function get available attacks for the combat system
def getAvailableAttacks(player):
    if not player.weapon:
        return [{
            "name": "Punch",
            "cost": 0,
            "min": 2,
            "max": 10
        }]
    # Weapon equipped 
    if player.attacks and len(player.attacks) > 0:
        return player.attacks
    # fallback if weapon equipped and class has no attacks
    return [{
            "name": f"{player.weapon.name} Strike",
            "cost": 0,
            "min": 5,
            "max": 10
    }]
# function choose attack
def chooseAttack(self): 
    attacks = getAvailableAttacks(self.player)
    lines = []
    for i, attack in enumerate(attacks, 1):
        costText = f" {attack['cost']} {self.player.resourceName}" if attack['cost'] > 0 else ""
        lines.append(f"[{i}] {attack['name']} - {attack['min']} - {attack['max']} damage{costText}")
    runawayOptionNumber = len(attacks) + 1
    lines.append("")
    lines.append(f"[{runawayOptionNumber}] Run away!")
    panel("Choose Attack", lines)
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and int(choice) == runawayOptionNumber: # run away if last option selected
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(attacks):
            return attacks[int(choice) - 1]
        print("Invalid choice")   
# function attack   
def attack(self, index=0):
    from Engine.setup import gameOverMenu
    room = self.dungeon[self.player.pos]
    if not room.enemies:
        print("Nothing to attack")
        return 
    if index < 0 or index >= len(room.enemies):
        print("Invalid enemy number")
        return       
    enemy = room.enemies[index]             
    print(f"You engaged {enemy.name} in combat")
    while enemy.alive() and self.player.hp > 0:
        panel(title=enemy.name, lines=[f"HP {enemy.hp}/{enemy.maxHP}"], footer=False)
        stats(self)
        attackMove = chooseAttack(self)
        if attackMove is None: # run away option
            print(f"You fled the fight against {enemy.name}")
            return 
        if self.player.resource < attackMove['cost']:
            print(f"Not enough {self.player.resourceName}")
            continue
        damage = random.randint(attackMove['min'], attackMove['max'])
        if self.player.weapon:
            damage += self.player.weapon.power
        enemy.hp -= damage 
        print(f"\nYou used {attackMove['name']} and dealt {damage} damage against {enemy.name}")
        if enemy.hp <= 0:
            print(f"You have slain {enemy.name}")
            self.player.gainXP(enemy.xp)
            room.enemies.remove(enemy)
            if room.boss:
                print("\nYou have cleared the dungeon!")
                gameOverMenu(self)
                return 
            return
        if enemy.alive():
            enemyDamage = random.randint(enemy.minDamage, enemy.maxDamage)
            self.player.hp -= enemyDamage
            print(f"{enemy.name} hits you for {enemyDamage} damage")
            if self.player.hp <= 0:
                print(f"You were slain by {enemy.name}...")
                gameOverMenu(self)
                return 