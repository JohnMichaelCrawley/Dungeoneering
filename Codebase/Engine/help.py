"""
Name: Help
Filename: help.py
Date Created: 23rd Jan 2026
Description:

This file outputs the commands when the player enters
'help'
"""
    # Help command to learn about other commannds
def help(self):
        print("""
Help:
###################
Command list:
    - go (north, south, east, west)
    - look (see what's in the room)
    - attack ('attack' just attacks the first thing in the room, otherwise, 'attack [value]' attacks enemy based on enemy number)
    - iventory / i (check your inventory)
    - eat 
    - drink
    - take (take + item = goes to your inventory)
    - map (check the map and where you are)
    - stats (check the character stats)
    - save (save the game and your progress)
###################""")

