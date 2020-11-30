def createNewGame(sesskey=None) -> dict:
    """
    Adds a new game of battleship to the database.

    #### Parameters
            sesskey (int): 
                Overwrite the previous game if the sesskey already exists.

    #### Returns
            A dict reprisentation of the game, ready to be exported as JSON.
    """