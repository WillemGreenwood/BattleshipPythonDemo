from ..common import PLAYER_TWO_SHOT_MASK
from ..common import SHIP_SIZE
from .battleship import validateShipConfig
from ..models.game_state_model import GameStateModel
from random import Random

r = Random()

def generateShips() -> dict:
    '''Generates a non-overlaping configuration of ships.'''
    out = dict()
    for ship, size in SHIP_SIZE.items():
        out[ship] = {
            "index": r.randint(0, 99),
            "isVertical": bool(r.randint(0, 1))
        }
        while not validateShipConfig(out):
            out[ship]["index"] = r.randint(0, 100 - size * (10 if out[ship]["isVertical"] else 1))
    return out

def move(game: GameStateModel) -> tuple:
    '''Performs an AI move on the game (as player two). Returns the move made, and it's result.'''
    options = []
    for i in range(100):
        if game.grid_state[i] & PLAYER_TWO_SHOT_MASK:
            options.append(i)
    i = r.choice(options)
    return (i, game.move_player_two(i))
