import app.services.battleship as battleship
import unittest

class battleship_test(unittest.TestCase):
    def setUp(self):
        self.ships = {
                "carrier"    : {
                    "index": 0,
                    "isVertical": True
                },
                "battleship" : {
                    "index": 1,
                    "isVertical": True
                },
                "cruiser"    : {
                    "index": 2,
                    "isVertical": True
                },
                "submarine"  : {
                    "index": 3,
                    "isVertical": True
                },
                "destroyer"  : {
                    "index": 4,
                    "isVertical": True
                }
            }

    def test_validate_ship_config_passes(self):
        self.assertTrue(battleship.validateShipConfig(self.ships))

    def test_validate_ship_config_fails_on_collision(self):
        temp = self.ships["submarine"]["isVertical"]
        self.ships["submarine"]["isVertical"] = False
        self.assertFalse(battleship.validateShipConfig(self.ships))
        self.ships["submarine"]["isVertical"] = temp

    def test_validate_ship_config_fails_on_out_of_bounds(self):
        temp = self.ships["submarine"]["index"]
        self.ships["submarine"]["index"] = 80
        self.assertFalse(battleship.validateShipConfig(self.ships))
        self.ships["submarine"]["index"] = temp
