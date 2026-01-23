"""
Name: XP For Level
Filename: xpforlevel.py
Date Created: 21 Jan 2026
Description:
I used the minimum total xp needed for a given level equation from [1], where you
can also see the growth needed to become maxed level

[1] - https://runescape.wiki/w/Experience#Equations
"""
def xpForLevel(L):
    gamma = 0.5772156649
    return int(
        (L**2)/8
        - (9/40)*L
        + 75 * (2 ** (L/7))
        - (75 * (2 ** (1/7))) / ((2 ** (1/7)) - 1)
        - gamma)