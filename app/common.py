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
    "carrier" : 5,
    "battleship" : 4,
    "cruiser" : 3,
    "submarine" : 3,
    "destroyer" : 2
}