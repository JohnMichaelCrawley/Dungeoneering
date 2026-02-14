"""
Name: Combat
Filename: combat.py
Date Created: 23rd Jan 2026
Description:

This file handles the combat system

"""
import random
from Engine.stats import stats


# get Available Attacks for the player
def getAvailableAttacks(player):
    # No weapons = punching only
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

# Let the player choose the attack:
def chooseAttack(self):
    attacks = getAvailableAttacks(self.player)
    print("\nChoose an attack:")
    for i, attack in enumerate(attacks, 1):
        costText = f" {attack['cost']} {self.player.resourceName}" if attack['cost'] > 0 else ""
        print(f"[{i}] {attack['name']} - {attack['min']} - {attack['max']} damage{costText}")
    runawayOptionNumber = len(attacks) + 1
    print(f"[{runawayOptionNumber}] Run away!")
    while True:
        choice = input("> ").strip()
        # run away if last option selected
        if choice.isdigit() and int(choice) == runawayOptionNumber:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(attacks):
            return attacks[int(choice) - 1]
        print("Invalid choice")
# Attack enemy    
def attack(self, index=0):
    from Engine.setup import gameOverMenu
    PANELWIDTH = 70
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
        # Enemy 
        print("#" * PANELWIDTH)
        print(f"| {enemy.name} |")
        print(f"| HP {enemy.hp}/{enemy.maxHP} |")
        print("-" * PANELWIDTH)
        
        # Player info 
        stats(self)
        
        # choose attack 
        attackMove = chooseAttack(self)
        # run away option
        if attackMove is None:
            print(f"You fled the fight against {enemy.name}")
            return 
        # resource check
        if self.player.resource < attackMove['cost']:
            print(f"Not enough {self.player.resourceName}")
            continue
        
        ### Damage roll 
        damage = random.randint(attackMove['min'], attackMove['max'])
        if self.player.weapon:
            damage += self.player.weapon.power
        enemy.hp -= damage 
        print(f"\nYou used {attackMove['name']} and dealt {damage} damage against {enemy.name}")
        # enemy defeated
        if enemy.hp <= 0:
            print(f"You have slain {enemy.name}")
            self.player.gainXP(enemy.xp)
            room.enemies.remove(enemy)
            if room.boss:
                print("\nYou have cleared the dungeon!")
                gameOverMenu(self)
                return 
            return
        # enemy turn 
        if enemy.alive():
            enemyDamage = random.randint(enemy.minDamage, enemy.maxDamage)
            self.player.hp -= enemyDamage
            print(f"{enemy.name} hits you for {enemyDamage} damage")
            if self.player.hp <= 0:
                print(f"You were slain by {enemy.name}...")
                gameOverMenu(self)
                return 
        
        
        