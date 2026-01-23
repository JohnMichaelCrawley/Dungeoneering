"""
Name: Commands
Filename: commands.py
Date Created: 21 Jan 2026
Description:
This file is used to help with commands for the text adventure game, for example:
player enters either "i" or "inventory" and the game will load up their inventory 
and display it to the player
"""
class Commands:
    def __init__(self, game):
        self.game = game
    # execute the command
    def execute(self, cmd):
        if not cmd:
            return
        match cmd[0]:
            case "help":
                self.game.help()
            case "go":
                direction = cmd[1] if len(cmd) > 1 else None
                if not direction: 
                    print ("Go where?\n(north, south, east, west)")
                    return 
                self.game.move(cmd[1])
            case "look":
                self.game.look()
            case "attack":
               if len(cmd) > 1 and cmd[1].isdigit():
                   self.game.attack(int(cmd[1]) - 1)
               else:
                   self.game.attack()
            case "inventory" | "i":
                self.game.inventory()     
            case "take":
                if len(cmd) < 2:
                    print("Take what?")
                else:
                    self.game.take(" ".join(cmd[1:]))                 
            case "drop":
                if len(cmd) < 2:
                    print("Drop what?")
                else:
                    self.game.drop(" ").join(cmd[1:])
            case "equip":
                if len(cmd) < 2:
                    print("Equip what?")
                else:
                    self.game.equip(" ".join(cmd[1:]))
            case "eat":
                if len(cmd) < 2:
                    print("Eat what?")
                else:
                    self.game.eat(" ".join(cmd[1:]))
            case "drink":
                if len(cmd) < 2:
                    print("drink what?")
                else:
                    self.game.drink(" ".join(cmd[1:]))
            case "use":
                self.game.use(cmd[1])   
            case "map":
                self.game.map()
            case "stats":
                self.game.stats()
            case "quit" | "exit" | "q":
                print("Saving game progress...")
                self.game.save()
                print("Progress saved")
                exit()
            case "save":
                print("Saving progress...")
                self.game.save()
                print("Game saved!")
            case _:
                print("Unknown command")