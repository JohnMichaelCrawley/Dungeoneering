"""
Name: Movement
Filename: movement.py
Date Created: 23rd Jan 2026
Description:

This file handles the player's movement throughout the 
dungeon 

"""
# function Move somewhere
def move(self, direction):
    x, y = self.player.pos
    directions = { 
        "north":(0, -1), 
        "south":(0, 1), 
        "west":(-1, 0), 
        "east":(1, 0) 
    }
    dx, dy = directions.get(direction, (0, 0))
    newPOS = (x+dx, y+dy)
    
    if newPOS not in self.dungeon:
        # self.player.pos = newPOS
        #self.dungeon[newPOS].visited = True
        #self.look()
        print("You hit a wall")
        return   
    # locked room check
    room = self.dungeon[newPOS]
    if room.boss and room.locked:
        hasKey = any(item.name == "Boss Key" for item in self.player.inventory)
        if not hasKey:
            print("The door is locked. You need to find the key to enter")
            return
        else:
            print("You unlocked the massive door")
            room.locked = False
    # move player
    self.player.pos = newPOS
    room.visited = True
    self.look()    