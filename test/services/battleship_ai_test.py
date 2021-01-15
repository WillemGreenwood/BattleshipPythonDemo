import app.services.battleship_ai as battleship_ai
from app.services.battleship import validateShipConfig
import unittest

class battleship_ai_test(unittest.TestCase):
    def test_generate_ships(self):
        self.assertTrue(validateShipConfig(battleship_ai.generateShips()))
