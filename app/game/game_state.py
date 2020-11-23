class Ship:
    def __init__(self, index: int, size: int, isVertial: bool):
        self.index = index
        self.size = size
        self.isVertial = isVertial

    def __repr__(self):
        return f"Ship(index={self.index}, size={self.size}, isVertical={self.isVertical})"


class PlayerConfig:
    def __init__(self, carrierIndex: int, carrierIsVertical: bool, battleshipIndex: int, battleshipIsVertical: bool, cruiserIndex: int, cruiserIsVertical: bool, submarineIndex: int, submarineIsVertical: bool, destroyerIndex: int, destroyerIsVertical: bool):
        self.ship = {
            "carrier" : Ship(carrierIndex, 5, carrierIsVertical),
            "battleship" : Ship(battleshipIndex, 4, battleshipIsVertical),
            "cruiser" : Ship(cruiserIndex, 3, cruiserIsVertical),
            "submarine" : Ship(submarineIndex, 3, submarineIsVertical),
            "destroyer" : Ship(destroyerIndex, 2, destroyerIsVertical) 
        }
        self.__collision_check__(10, 10)

    def __collision_check__(self, width: int, height: int):
        indices = set()
        count = 0
        for _,ship in self:
            for i in range(ship.size):
                index = ship.index + (width if ship.isVertial else 1) * i
                if index < 0 or index >= width * height:
                    IndexError(f"Invalid config, ship {ship} does not fit on {width}x{height} game board.")
                indices.add(ship.index + width * i)
        if len(indices) is not count:
            raise IndexError("Two or more ships occupy the same space.")


    def __iter__(self):
        return self.ship.items().__iter__()


class Game:
    def __init__(self, p1_pieces: PlayerConfig, p2_pieces: PlayerConfig):
        self.p1_pieces = p1_pieces
        self.p2_pieces = p2_pieces
        self.p1_ships = 5
        self.p1_ship_health = {
            "ships" : 5,
            "carrier" : 5,
            "battleship" : 4,
            "cruiser" : 3,
            "submarine" : 3,
            "destroyer" : 2
        }
        self.p2_ships = 5
        self.p2_ship_health = {
            "ships" : 5,
            "carrier" : 5,
            "battleship" : 4,
            "cruiser" : 3,
            "submarine" : 3,
            "destroyer" : 2
        }
        self.state_grid = [[False,False,"",""] for i in range(100)]

        for name, ship in p1_pieces:
            for i in range(ship.size):
                index = ship.index + (10 if ship.isVertial else 1) * i
                self.state_grid[index][2] = name
        for name, ship in p2_pieces:
            for i in range(ship.size):
                index = ship.index + (10 if ship.isVertial else 1) * i
                self.state_grid[index][3] = name
            
    def p1_move(self, index):
        if index < 0 or index >= 100:
            raise IndexError(f"Move {index} outside game bounds!")
        if self.state_grid[index][0]:
            raise IndexError(f"Move {index} already occured!")
        
        self.state_grid[index][0] = True
        
        ship_name = self.state_grid[index][3]
        if ship_name:
            self.p2_ship_health[ship_name] -= 1
            if self.p2_ship_health[ship_name] is 0:
                self.p2_ships -= 1
                return f"sunk_{ship_name}"
            return "hit"

        return "miss"

    def p2_move(self, index):
        if index < 0 or index >= 100:
            raise IndexError(f"Move {index} outside game bounds!")
        if self.state_grid[index][0]:
            raise IndexError(f"Move {index} already occured!")
        
        self.state_grid[index][1] = True
        
        ship_name = self.state_grid[index][2]
        if ship_name:
            self.p1_ship_health[ship_name] -= 1
            if self.p1_ship_health[ship_name] is 0:
                self.p1_ships -= 1
                return f"sunk_{ship_name}"
            return "hit"

        return "miss"

    def game_victor(self):
        if self.p2_ships is 0:
            return "p1"
        elif self.p1_ships is 0:
            return "p2"
        return None
