
"""
Name: Stats
Filename: stats.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the character's stats like health, name and class
"""

# See player stats  
def stats(self):
    print("##############################")
    print(f"""{self.player.name} the {self.player.playerClass} \n - Level: {self.player.level}  \n - XP: {self.player.xp} \n - HP: {self.player.hp}/{self.player.maxHP}""")
    print("##############################")