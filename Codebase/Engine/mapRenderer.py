"""
Name: Map Renderer
Filename: maprenderer.py
Date Created: 23rd Jan 2026
Description:

This file handles the output of the current map the player is on
and displays the map to the player with the command 'map'

"""
from Engine.ui import panel
# function See dungeon map ▼
def map(self):
    panel("Icons", ["▼ - Player", "x - Room visited", "B - Boss room"])
    width = self.mapSize
    # build the horzintaol grid row dynamically
    horizontal = "+" + "---+" * width
    # frame width based on grid
    framedWidth = len("## " + horizontal + " ##")
    # border line
    border = "#" * framedWidth
    print("\nDungeon Map:")
    # Top border
    print(border+"\n"+border)
    for y in range(width):
        print("## " + horizontal + " ##")
        # Room row
        row = "## |"
        for x in range(width):
            room = self.dungeon.get((x, y))
            if (x, y) == self.player.pos:
                row += " ▼ |"
            elif (x, y) in self.dungeon and self.dungeon[(x, y)].visited:
                row += " x |"
            elif room and room.discoveredBossRoom:
                row += " B |"
            else:
                row += "   |"
        row += " ##"
        print(row)
    # bottom grid seperator
    print("## " + horizontal + " ##")
    print(border+"\n"+border) 