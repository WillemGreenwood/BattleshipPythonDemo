from .. import db
from ..common import PLAYER_ONE_SHOT_MASK
from ..common import PLAYER_TWO_SHOT_MASK
from ..common import PLAYER_ONE_SHIP_ID_MASK
from ..common import PLAYER_TWO_SHIP_ID_MASK
from ..common import SHIP_ID_MAPPING
from ..common import SHIP_SIZE
from datetime import datetime

class GameStateModel(db.Model):
    """lorem ipsum"""

    __tablename__ = "gamestates"

    # User ID for the user, primary key
    user_id = db.Column(
        "user_id",
        db.String(16),
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
            self.player_two_ships = self.player_two_ships[:ship_id * 3 - 1] + chr(ord(self.player_two_ships[ship_id * 3 - 1]) - 1) + self.player_two_ships[ship_id * 3:]
            if ord(self.player_two_ships[ship_id * 3 - 1]) == 0:
                self.player_two_ships = chr(ord(self.player_two_ships[0]) - 1) + self.player_two_ships[1:]
                hit_result = f"sunk_{[k for k,v in SHIP_ID_MAPPING.items() if v == ship_id][0]}"

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
            self.player_one_ships = self.player_one_ships[:ship_id * 3 - 1] + chr(ord(self.player_one_ships[ship_id * 3 - 1]) - 1) + self.player_one_ships[ship_id * 3:]
            if ord(self.player_one_ships[ship_id * 3 - 1]) == 0:
                self.player_one_ships = chr(ord(self.player_one_ships[0]) - 1) + self.player_one_ships[1:]
                hit_result = f"sunk_{[k for k,v in SHIP_ID_MAPPING.items() if v == ship_id][0]}"

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
                    "index": ord(shipstr[v*3 - 2]),
                    "isVertical": (shipstr[v*3] == "v")
                }
            return out
        
        return {
            "player_ships": decode_ships(self.player_one_ships),
            "opponent_ships": decode_ships(self.player_two_ships),
            "grid": [ord(i) & (PLAYER_ONE_SHOT_MASK | PLAYER_TWO_SHOT_MASK) for i in self.grid_state]
        }


    @classmethod
    def newGame(cls, player_one: dict, player_two: dict):
        '''Creates a new game.'''
        out = GameStateModel()

        out.player_one_ships = chr(5)
        for ship in ("carrier", "battleship", "cruiser", "submarine", "destroyer"):
            out.player_one_ships += chr(player_one[ship]["index"]) + chr(SHIP_SIZE[ship]) + ("v" if chr(player_one[ship]["isVertical"]) else "h")

        out.player_two_ships = chr(5)
        for ship in ("carrier", "battleship", "cruiser", "submarine", "destroyer"):
            out.player_two_ships += chr(player_two[ship]["index"]) + chr(SHIP_SIZE[ship]) + ("v" if chr(player_two[ship]["isVertical"]) else "h")

        out.grid_state = chr(0) * 100

        for k, v in player_one.items():
            for cell in [v["index"] + (i * 10 if v["isVertical"] else 1) for i in range(SHIP_SIZE[k])]:
                out.grid_state = out.grid_state[:cell] + chr(SHIP_ID_MAPPING[k] << 2) + out.grid_state[cell+1:]

        for k, v in player_two.items():
            for cell in [v["index"] + (i * 10 if v["isVertical"] else 1) for i in range(SHIP_SIZE[k])]:
                out.grid_state = out.grid_state[:cell] + chr(ord(out.grid_state[cell]) + (SHIP_ID_MAPPING[k] << 5)) + out.grid_state[cell+1:]

        return out
