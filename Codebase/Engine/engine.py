"""
Name: Engine
Filename: engine.py
Date Created: 23rd Jan 2026
Description:
This is the main initialiser class for the game engine
"""
from Engine.dungeon import createDungeon
from Engine.movement import move
from Engine.combat import attack
from Engine.actions import look, take, drop, eat, drink, equip, consumeItemForPlayer
from Engine.help import help
from Engine.inventory import inventory
from Engine.mapRenderer import map
from Engine.stats import stats
from Engine.saveSystem import save, checkForSaveFile
from Engine.setup import setupNewGame, clearScreenOutput
from jsonLoader import loadEnemiesToGame, loadItemsToGame
from Engine.mapSizeConfig import MAPSIZES
from Engine.dungeon import createDungeon, spawnEnemies, createFinalBoss
from Commands.Command import Commands

class GameEngine:
    # initialise the game
    def __init__(self):
        self.dungeon = {}
        self.player = None
        self.enemyTemplates = list(loadEnemiesToGame()["enemies"])
        self.itemData = loadItemsToGame()
        # set map default size
        self.mapSize = MAPSIZES["medium"]
        # BIND engine actions 
        self.createDungeon = createDungeon.__get__(self)
        self.move = move.__get__(self)
        self.attack = attack.__get__(self)
        self.look = look.__get__(self)
        self.consumeItemForPlayer = consumeItemForPlayer.__get__(self)
        self.take = take.__get__(self)
        self.drop = drop.__get__(self)
        self.eat = eat.__get__(self)
        self.drink = drink.__get__(self)
        self.equip = equip.__get__(self)
        self.help = help.__get__(self)
        self.inventory = inventory.__get__(self)
        self.map = map.__get__(self)
        self.stats = stats.__get__(self)
        self.save = save.__get__(self).__get__(self)
        self.checkForSaveFile = checkForSaveFile.__get__(self)
        self.setupNewGame = setupNewGame.__get__(self)
        self.clearScreenOutput = clearScreenOutput.__get__(self)
        self.spawnEnemies = spawnEnemies.__get__(self)
        self.createFinalBoss = createFinalBoss.__get__(self)
        self.commands = Commands(self)
        
    # Game title     
    def title(self):
        print("""
    ██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗ ███████╗ ███████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗
    ██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗████╗  ██║ ██╔════╝ ██╔════╝██╔═══██╗██╔══██╗██║████╗  ██║██╔════╝
    ██║  ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██╔██╗ ██║ █████╗   █████╗  ██║   ██║██████╔╝██║██╔██╗ ██║██║  ███╗
    ██║  ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║╚██╗██║ ██╔══╝   ██╔══╝  ██║   ██║██╔══██╗██║██║╚██╗██║██║   ██║
    ██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██║ ╚████║ ███████╗ ███████╗╚██████╔╝██║  ██║██║██║ ╚████║╚██████╔╝
    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚══════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝

    Version: [In-Development] | Date released: [] | Last Update: []

    DUNGEONEERING: Text Adventure Game by John Crawley, build using Python & JSON as a fun project to work on

    The purpose of this text adventure game is to explore the dungeon, grow stronger by finding items, defeating enemies and 
    then find a key to enter the boss room and defeat it.

    If you require help, enter the command 'help' and it will display a list of commands you can use in this game


    - John Crawley © 2026 - 
    """)