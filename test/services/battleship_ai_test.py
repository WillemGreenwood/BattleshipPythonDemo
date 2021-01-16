import app.services.battleship_ai as battleship_ai
from app.models.game_state_model import GameStateModel
from app.services.battleship import validateShipConfig
import unittest

class battleship_ai_test(unittest.TestCase):
    def test_generate_ships(self):
        """ WARNING: The function being tested is random, so this test is
            fundimentaly unstable. It should however pass in all instances.
        """
        self.assertTrue(validateShipConfig(battleship_ai.generateShips()))

    def test_move(self):
        """ WARNING: The function being tested is random, so this test is
            fundimentaly unstable. It should however pass in all instances.
        """
        game = mock_game("\x00", "moveout")
        move, result = battleship_ai.move(game)
        self.assertEqual("moveout", result)

class mock_game:
    def __init__(self, cell, expected):
        self.grid_state = cell * 100
        self.__expected = expected

    def move_player_two(self, i):
        return self.__expected