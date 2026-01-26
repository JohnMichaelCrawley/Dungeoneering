"""
Name: Main 
Filename: main.py
Date Created: 21 Jan 2026
Description:
This file is the main area where the game actually is run through and 
creating the game loop
"""
from Engine.engine import GameEngine
# Main 
def main():
    game = GameEngine()
    game.title()
    game.checkForSaveFile()   
if __name__ == "__main__":
        main() 