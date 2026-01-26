
"""
Name: Stats
Filename: stats.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the character's stats like health, name and class
"""

PANELWIDTH = 70
# See player stats  
def stats(self):
    print("#" * PANELWIDTH)
    print(f"| {"Player Stats".ljust(PANELWIDTH - 4)} |")
    print("-" * PANELWIDTH)
    
    statsLine = [
        f"{self.player.name} the {self.player.playerClass}",
        f"Level: {self.player.level}",
        f"XP: {self.player.xp}",
        f"HP: {self.player.hp}/{self.player.maxHP}"
    ]
    
    for line in statsLine:
        print(f"| {line.ljust(PANELWIDTH -4)} |")

    print("#" * PANELWIDTH)
    print()