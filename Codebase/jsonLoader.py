"""
Name: JSON Loader
Filename: jsonloader.py
Date Created: 22 Jan 2026
Description:
This file gets the data from the JSON files and bring the data into the game
"""
import os
import json 

def loadJsonFileToGame(file):
    baseDir = os.path.dirname(__file__)
    path = os.path.join(baseDir, "data", file)
    with open (path, "r") as f:
        return json.load(f)

# load player classes into the game
def loadPlayerClasses():
    return loadJsonFileToGame("PlayerClasses.json")
# load Enemies to the Game
def loadEnemiesToGame():
    return loadJsonFileToGame("Enemies.json")
# load Items To the Game
def loadItemsToGame():
    return loadJsonFileToGame("Items.json")
    
