"""
Name: Help
Filename: help.py
Date Created: 23rd Jan 2026
Description:

This file outputs the commands when the player enters
'help'
"""

PANELWIDTH = 70 
COMMANDCOLWIDTH = 26 # controls align column
commands = [
    ("[go] <direction>", "Move <north>, <south>, <east>, <west>"),
    ("[look]", "Inspect the current room"),  
    ("[attack] <n>", "Attack enemy number"),  
    ("[inventory] / [i]", "Open your inventory"),
    ("[take] <item> / [take all]", "Pick up an item"),  
    ("[eat] <food>", "Eat food to restore HP"),  
    ("[drink] <potion>", "Drink to restore or increase stats"), 
    ("[equip] <weapon", "Equip your player class weapon"),
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
# Help command to learn about other commannds
def help(self):
    print("\n")
    print("#" * PANELWIDTH)
    print(f"| {'Help - Command list'.ljust(PANELWIDTH - 4)} |")
    print("-" * PANELWIDTH)
    # print command list
    for command, description in commands:
        commandPadded = command.ljust(COMMANDCOLWIDTH)
        line = f"{commandPadded} - {description}"
        print(f"| {line.ljust(PANELWIDTH -4)} |")
    print("-" * PANELWIDTH)
    # show examples
    print(f"| {'Examples:'.ljust(PANELWIDTH - 4)} |")
    for example in examples:
        exampleLine = f"-{example}"
        print(f"| {exampleLine.ljust(PANELWIDTH - 4)} |")
    print("#" * PANELWIDTH)
    print("\n")