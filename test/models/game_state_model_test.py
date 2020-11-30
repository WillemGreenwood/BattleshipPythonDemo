from app.models.game_state_model import GameStateModel
from app.models.game_state_model import newGame
import unittest

class GameStateModelTest(unittest.TestCase):

    def setUp(self):
        self.game = GameStateModel()
        # All ships ligned up verticaly, largest in top left corner, moving right.
        self.game.player_one_ships = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x02"
        self.game.player_two_ships = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x02"
        self.game.grid_state = "".join((
            "\x24\x48\x6c\x90\xb4\x00\x00\x00\x00\x00",
            "\x24\x48\x6c\x90\xb4\x00\x00\x00\x00\x00",
            "\x24\x48\x6c\x90\x00\x00\x00\x00\x00\x00",
            "\x24\x48\x00\x00\x00\x00\x00\x00\x00\x00",
            "\x24\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        ))

    def test_move_player_one_moves_correct_index(self):
        self.game.move_player_one(3+3*10)
        self.game.move_player_one(3+8*10)
        self.game.move_player_one(7+3*10)
        self.game.move_player_one(7+8*10)
        self.assertEqual('\x01', self.game.grid_state[3+3*10])
        self.assertEqual('\x01', self.game.grid_state[3+8*10])
        self.assertEqual('\x01', self.game.grid_state[7+3*10])
        self.assertEqual('\x01', self.game.grid_state[7+8*10])

    def test_move_player_two_moves_correct_index(self):
        self.game.move_player_two(3+3*10)
        self.game.move_player_two(3+8*10)
        self.game.move_player_two(7+3*10)
        self.game.move_player_two(7+8*10)
        self.assertEqual('\x02', self.game.grid_state[3+3*10])
        self.assertEqual('\x02', self.game.grid_state[3+8*10])
        self.assertEqual('\x02', self.game.grid_state[7+3*10])
        self.assertEqual('\x02', self.game.grid_state[7+8*10])

    def test_move_player_one_returns_miss(self):
        pass

    def test_move_player_two_returns_miss(self):
        pass

    def test_move_player_one_returns_hit(self):
        pass

    def test_move_player_two_returns_hit(self):
        pass

    def test_move_player_one_returns_sunk(self):
        pass

    def test_move_player_two_returns_sunk(self):
        pass

    def test_move_player_one_updates_ship_health(self):
        pass

    def test_move_player_two_updates_ship_health(self):
        pass

    def test_move_player_one_updates_ships_remaining(self):
        pass

    def test_move_player_two_updates_ships_remaining(self):
        pass

class FunctionsTest(unittest.TestCase):
    pass
