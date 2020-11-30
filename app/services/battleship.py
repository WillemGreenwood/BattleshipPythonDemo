from ..common import SHIP_SIZE

def createNewGame(sesskey=None) -> dict:
    """
    Adds a new game of battleship to the database.

    #### Parameters
            sesskey (int): 
                Overwrite the previous game if the sesskey already exists.

    #### Returns
            A dict reprisentation of the game, ready to be exported as JSON.
    """

def validateShipConfig(ships: dict) -> bool:
    '''Verify that a given configuration of ships is valid (no overlaps).'''
    space = set()
    spaces = 0

    for ship, conf in ships.items():
        for i in range(SHIP_SIZE[ship]):
            index = i * (10 if conf['isVertical'] else 1) + conf['index']
            space.add(index)
            spaces += 1
            if not (0 <= index <= 99) or len(space) < spaces:
                return False

    return True
