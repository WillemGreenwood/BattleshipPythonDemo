from .. import db
from ..game.game_state import Game
from datetime import datetime

PLAYER_ONE_SHOT_MASK = 0b00000001
PLAYER_TWO_SHOT_MASK = 0b00000010
PLAYER_ONE_SHIP_ID_MASK = 0b00011100
PLAYER_TWO_SHIP_ID_MASK = 0b11100000
SHIP_ID_MAPPING = {
    "carrier"    : 0b001,  # 1
    "battleship" : 0b010,  # 2
    "cruiser"    : 0b011,  # 3
    "submarine"  : 0b100,  # 4
    "destroyer"  : 0b101   # 5
}
SHIP_SIZE = {
    "ships" : 5,
    "carrier" : 5,
    "battleship" : 4,
    "cruiser" : 3,
    "submarine" : 3,
    "destroyer" : 2
}

class GameStateModel(db.Model):
    """lorem ipsum"""

    __tablename__ = "gamestates"

    # Session ID for the user, primary key
    sesskey = db.Column(
        "sesskey",
        db.Integer,
        primary_key=True
    )

    # Ship indexes and orientations for player one.
    # Includes ship health and ships remaining.
    # First char is the number of ships remaining,
    # then for each of the following chars, the first
    # is the index of the ship, the second is the 
    # orientation (v vs h), and the third is the
    # ship's remaining health.
    player_one_ships = db.Column(
        "player_one_ships",
        db.String(16)
    )

    # Ship indexes and orientations for player two.
    # Includes ship health and ships remaining.
    # First char is the number of ships remaining,
    # then for each of the following chars, the first
    # is the index of the ship, the second is the 
    # orientation (v vs h), and the third is the
    # ship's remaining health.
    player_two_ships = db.Column(
        "player_two_ships",
        db.String(16)
    )

    # The grid of the game state
    # String is 100 chars, each char is an 8-bit
    # representation of the state of that cell
    # in the grid. The rightmost bit is if p1
    # has fired on that cell, second is if p2
    # has fired, next three are the id of p1's
    # ship if one intersects that cell, and the
    # last three are the same for p2.
    grid_state = db.Column(
        "grid_state",
        db.String(100)
    )

    # The last time this entry was updated,
    # used to cull old entries
    last_updated = db.Column(
        "last_updated",
        db.DateTime()
    )

    def move_player_one(self, i: int):
        '''Simulate a shot fired by p1, returns True if hit, False if miss, None if shot already fired'''
        cell = ord(self.grid_state[i])
        
        # Move has already been made?
        if cell & PLAYER_ONE_SHOT_MASK:
            return None

        # Hit p2 ship?
        hit_result = "miss"
        if cell & PLAYER_TWO_SHIP_ID_MASK:
            ship_id = (cell & PLAYER_TWO_SHIP_ID_MASK) >> 5
            self.player_two_ships = self.player_two_ships[:1 + ship_id * 3] + chr(ord(self.player_two_ships[1 + ship_id * 3]) - 1) + self.player_two_ships[2 + ship_id * 3:]
            if ord(self.player_two_ships[1 + ship_id * 3]) == 0:
                self.player_two_ships = chr(ord(self.player_two_ships[0]) - 1) + self.player_two_ships[1:]
                hit_result = f"sunk_{[k for k,v in SHIP_SIZE.items() if v == ship_id][0]}"

        # Apply move
        self.grid_state = self.grid_state[:i] + chr(cell | PLAYER_ONE_SHOT_MASK) + self.grid_state[i+1:]
        return hit_result

    def move_player_two(self, i: int):
        '''Simulate a shot fired by p1, returns True if hit, False if miss, None if shot already fired'''
        cell = ord(self.grid_state[i])
        
        # Move has already been made?
        if cell & PLAYER_TWO_SHOT_MASK:
            return None

        # Hit p1 ship?
        hit_result = "miss"
        if cell & PLAYER_ONE_SHIP_ID_MASK:
            ship_id = (cell & PLAYER_ONE_SHIP_ID_MASK) >> 2
            self.player_one_ships = self.player_one_ships[:1 + ship_id * 3] + chr(ord(self.player_one_ships[1 + ship_id * 3]) - 1) + self.player_one_ships[2 + ship_id * 3:]
            if ord(self.player_one_ships[1 + ship_id * 3]) == 0:
                self.player_one_ships = chr(ord(self.player_one_ships[0]) - 1) + self.player_one_ships[1:]
                hit_result = f"sunk_{[k for k,v in SHIP_SIZE.items() if v == ship_id][0]}"

        # Apply move
        self.grid_state = self.grid_state[:i] + chr(cell | PLAYER_TWO_SHOT_MASK) + self.grid_state[i+1:]
        return hit_result

    def markUpdate(self):
        self.last_updated = datetime.now()

    def getState(self) -> dict:
        '''Returns a dict/JSON-like format of this object'''
        def decode_ships(shipstr):
            out = dict()
            for k,v in SHIP_ID_MAPPING.items():
                out[k] = {
                    "index": ord(shipstr[1 + v*3]),
                    "isVertial": (shipstr[2 + v*3] == "v")
                }
            return out
        
        return {
            "player_ships": decode_ships(self.player_one_ships),
            "opponent_ships": decode_ships(self.player_two_ships),
            "grid": [ord(i) & (PLAYER_ONE_SHOT_MASK | PLAYER_TWO_SHOT_MASK) for i in self.grid_state]
        }


def newGame(player_one: dict, player_two: dict) -> GameStateModel:
    '''Creates a new game.'''
    out = GameStateModel()

    out.player_one_ships = chr(5)
    for ship in ("carrier", "battleship", "cruiser", "submarine", "destroyer"):
        out.player_one_ships += chr(player_one[ship]["index"]) + ("v" if chr(player_one[ship]["isVertical"]) else "h") + chr(SHIP_SIZE[ship])

    out.player_two_ships = chr(5)
    for ship in ("carrier", "battleship", "cruiser", "submarine", "destroyer"):
        out.player_two_ships += chr(player_two[ship]["index"]) + ("v" if chr(player_two[ship]["isVertical"]) else "h") + chr(SHIP_SIZE[ship])

    out.grid_state = chr(0) * 100

    for k, v in player_one.items():
        for cell in [v["index"] + (i * 10 if v["isVertical"] else 1) for i in range(SHIP_SIZE[k])]:
            out.grid_state = out.grid_state[:cell] + chr(SHIP_ID_MAPPING[k] << 2) + out.grid_state[cell+1:]

    for k, v in player_two.items():
        for cell in [v["index"] + (i * 10 if v["isVertical"] else 1) for i in range(SHIP_SIZE[k])]:
            out.grid_state = out.grid_state[:cell] + chr(ord(out.grid_state[cell]) + (SHIP_ID_MAPPING[k] << 5)) + out.grid_state[cell+1:]

    return out
