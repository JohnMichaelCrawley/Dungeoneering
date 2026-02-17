"""
Name: Help
Filename: help.py
Date Created: 23rd Jan 2026
Description:

This file outputs the commands when the player enters
'help'
"""
from Engine.ui import panel
commands = [
    ("[go] <direction>", "Move <north>, <south>, <east>, <west>"),
    ("[look]", "Inspect the current room"),  
    ("[attack] <n>", "Attack enemy number"),  
    ("[inventory] / [i]", "Open your inventory"),
    ("[take] <item> / [take all]", "Pick up an item"),  
    ("[eat] <food>", "Eat food to restore HP"),  
    ("[drink] <potion>", "Drink to restore or increase stats"), 
    ("[equip] <weapon>", "Equip your player class weapon"),
    ("[map]", "View dungeon map"),
    ("[stats]", "View your character's stats"),  
    ("[save]", "Save your game progress")   
]
examples = [
    "go north",
    "attack 1",
    "take cooked meat",
    "inventory",
    "map",
    "stats"
]
# function Help command to learn about other commannds
def help(self):
    COMMANDCOLWIDTH = 26 # controls align column
    lines = []
    for command, description in commands:
        line = f"{command.ljust(COMMANDCOLWIDTH)} - {description}"
        lines.append(line)
    # spacing
    lines.append("---")
    lines.append("Examples:")
    for example in examples:
        lines.append(f"- {example}")
    panel("Help - Command List:", lines)
    
