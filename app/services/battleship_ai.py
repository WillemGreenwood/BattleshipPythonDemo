from ..common import SHIP_SIZE
from .battleship import validateShipConfig
from random import Random

r = Random()

def generateShips() -> dict:
    '''Generates a non-overlaping configuration of ships.'''
    out = dict()
    for ship, size in SHIP_SIZE.keys():
        out[ship] = {
            "index": r.randint(0, 99),
            "isVertical": bool(r.randint(0, 1))
        }
        while not validateShipConfig(out):
            out[ship]["index"] = r.randint(0, 100 - size * (10 if out[ship]["isVertical"] else 1))
    return out
