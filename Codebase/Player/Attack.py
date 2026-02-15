"""
Name: Attack
Filename: attack.py
Date Created: 21 Jan 2026
Description:
This is used to execute an attack on an enemy you're fighting in the game
"""
import random 
class Attack:
    def __init__(self, name, minDamage, maxDamage, cost, effect=None):
        pass
        self.name = name
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.cost = cost
        self.effect = effect
    # execute attack  
    def execute (self, player, enemy):
        if player.resource < self.cost:
            return f"Not enough {player.resourceName}"  
        player.resource -= self.cost
        damage = random.randint(self.minDamage, self.maxDamage)