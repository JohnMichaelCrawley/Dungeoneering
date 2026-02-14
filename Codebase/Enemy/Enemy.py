"""
Name: Enemy
Filename: eemy.py
Date Created: 22 Jan 2026
Description:
This file builds up the model of enemies by creating an init base value
and have return if alive is true or false
"""
class Enemy:
    def __init__(self, name, level, baseHP, baseAttack, baseXP):
        self.name = name
        self.level = level 
        
        self.maxHP = baseHP + (level * 4)
        self.hp = self.maxHP
        
        self.minDamage = baseAttack 
        self.maxDamage = baseAttack + 2
        
        self.attack = baseAttack + (level * 2)
        self.xp = baseXP + (level * 8)

        
    def alive (self):
        return self.hp > 0
        