
"""
Name: Stats
Filename: stats.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the character's stats like health, name and class
"""
from Engine.ui import panel
# See player stats  
def stats(self):
    lines = [
        f"{self.player.name} the {self.player.playerClass}",
        "----",
        f"Level: {self.player.level}",
        f"XP: {self.player.xp}",
        f"HP: {self.player.hp}/{self.player.maxHP}"
    ]
    panel("Player Stats:", lines)