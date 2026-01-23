"""
Name: Main 
Filename: main.py
Date Created: 21 Jan 2026
Description:
This file is the main area where the game actually is run through and 
creating the game loop
"""
import os
import json
from GameEngine import GameEngine
from Player.Player import Player
from Player.xpForLevel import xpForLevel
from jsonLoader import loadPlayerClasses
def main():
    game = GameEngine()
    game.title()
    game.checkForSaveFile()
    
    # Game is running and player runs commands
    while True:
        cmd = input("\n> ").lower().split()
        game.clearScreenOutput()
        game.title()
        if not cmd:
            continue
        game.commands.execute(cmd)
        
if __name__ == "__main__":
        main() 