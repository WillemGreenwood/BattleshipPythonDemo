from app.models.game_state_model import GameStateModel
from app.models.game_state_model import newGame
import unittest

class GameStateModelTest(unittest.TestCase):

    def setUp(self):
        self.game = GameStateModel()
        # All ships ligned up verticaly, largest in top left corner, moving right.
        self.game.player_one_ships = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x02v"
        self.game.player_two_ships = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x02v"
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

    def test_move_player_one_hit(self):
        expected_return = "miss"
        expected_ship_state = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x01v"

        actual_return = self.game.move_player_one(4+0*10)  # Row 0, Col 4
        actual_ship_state = self.game.player_two_ships

        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_ship_state, actual_ship_state)

    def test_move_player_one_miss(self):
        expected_return = "miss"
        expected_ship_state = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x02v"

        actual_return = self.game.move_player_one(3+3*10)  # Row 3, Col 3
        actual_ship_state = self.game.player_two_ships

        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_ship_state, actual_ship_state)

    def test_move_player_one_moves_correct_index(self):
        self.game.move_player_one(3+3*10)  # Row 3, Col 3
        self.game.move_player_one(3+8*10)  # Row 8, Col 3
        self.game.move_player_one(7+3*10)  # Row 3, Col 7
        self.game.move_player_one(7+8*10)  # Row 8, Col 7
        self.assertEqual('\x01', self.game.grid_state[3+3*10])  # Row 3, Col 3
        self.assertEqual('\x01', self.game.grid_state[3+8*10])  # Row 8, Col 3
        self.assertEqual('\x01', self.game.grid_state[7+3*10])  # Row 3, Col 7
        self.assertEqual('\x01', self.game.grid_state[7+8*10])  # Row 8, Col 7

    def test_move_player_one_sunk(self):
        expected_return = "sunk_destroyer"
        expected_ship_state = "\x04\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x00v"

        actual_return = self.game.move_player_one(4+0*10)  # Row 0, Col 4
        actual_return = self.game.move_player_one(4+1*10)  # Row 1, Col 4
        actual_ship_state = self.game.player_two_ships

        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_ship_state, actual_ship_state)

    def test_move_player_two_hit(self):
        expected_return = "miss"
        expected_ship_state = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x01v"

        actual_return = self.game.move_player_two(4+0*10)  # Row 0, Col 4
        actual_ship_state = self.game.player_one_ships

        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_ship_state, actual_ship_state)

    def test_move_player_two_miss(self):
        expected_return = "miss"
        expected_ship_state = "\x05\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x02v"

        actual_return = self.game.move_player_two(3+3*10)  # Row 3, Col 3
        actual_ship_state = self.game.player_one_ships

        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_ship_state, actual_ship_state)

    def test_move_player_two_moves_correct_index(self):
        self.game.move_player_two(3+3*10)  # Row 3, Col 3
        self.game.move_player_two(3+8*10)  # Row 8, Col 3
        self.game.move_player_two(7+3*10)  # Row 3, Col 7
        self.game.move_player_two(7+8*10)  # Row 8, Col 7
        self.assertEqual('\x02', self.game.grid_state[3+3*10])  # Row 3, Col 3
        self.assertEqual('\x02', self.game.grid_state[3+8*10])  # Row 8, Col 3
        self.assertEqual('\x02', self.game.grid_state[7+3*10])  # Row 3, Col 7
        self.assertEqual('\x02', self.game.grid_state[7+8*10])  # Row 8, Col 7

    def test_move_player_two_sunk(self):
        expected_return = "sunk_destroyer"
        expected_ship_state = "\x04\x00\x05v\x01\x04v\x02\x03v\x03\x03v\x04\x00v"

        actual_return = self.game.move_player_two(4+0*10)  # Row 0, Col 4
        actual_return = self.game.move_player_two(4+1*10)  # Row 1, Col 4
        actual_ship_state = self.game.player_one_ships

        self.assertEqual(expected_return, actual_return)
        self.assertEqual(expected_ship_state, actual_ship_state)

    def test_mark_update(self):
        # Build
        import app.models.game_state_model as gsm
        temp_datetime = gsm.datetime
        gsm.datetime = mock_datetime()
        expected = gsm.datetime.value()
        
        # Run
        self.game.markUpdate()
        actual = self.game.last_updated

        # Check
        self.assertEqual(expected, actual)

        # Teardown
        gsm.datetime = temp_datetime

class mock_datetime:
    def __init__(self):
        from datetime import datetime
        self.cargo = datetime.now()

    def value(self):
        return self.cargo

    def now(self):
        return self.value()

class FunctionsTest(unittest.TestCase):
    pass
