# BattleshipPythonDemo v0.0.0
Implementation standard of a Battleship game

## Endpoints

| URI | Method | Purpous |
| --- | --- | --- |
| `~/battleship` | `GET` | Get the current game state. |
| `~/battleship` | `PUT` | Create a new game. Should assign an ID cookie if one was not already established. |
| `~/battleship/move/<index>` | `PUSH` | If the move is valid, returns the results of the move, and the opponent's following move. If the move ends the game, includes the corrisponding flag. If the move is invalid, returns the appropriate flag. If the game specified by the request's cookies doesn't exist, returns `404 NOT FOUND`. |


## JSON Schimas

### [game_state_schima.json](./json_schimas/game_state_schima.json)
```JSON
{
    "$schema": "http://json-schema.org/draft/2019-09/schema#",
    "definitions": {
        "ships": {
            "type": "object",
            "properties": {
                "carrier": { "$ref": "#/definitions/ship" },
                "battleship": { "$ref": "#/definitions/ship" },
                "cruiser": { "$ref": "#/definitions/ship" },
                "submarine": { "$ref": "#/definitions/ship" },
                "destroyer": { "$ref": "#/definitions/ship" } 
            }
        },
        "ship": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 99
                },
                "isVertical": {
                    "type": "boolean"
                }
            }
        }
    },
    
    "type": "object",
    "properties": {
        "player_ships": { "$ref": "#/definitions/ships" },
        "opponent_ships": { "$ref": "#/definitions/ships" },
        "grid": {
            "type": "array",
            "items": {
                "type": "integer",
                "minimum": 0,
                "maximum": 15
            },
            "minItems": 100,
            "maxItems": 100
        }
    }
}
```

### [move_response_schima.json](./json_schimas/move_response_schima.json)
```JSON
{
    "$schema": "http://json-schema.org/draft/2019-09/schema#",
    "type": "object",
    "properties": {
        "moveResult": {
            "type": "string",
            "enum": [
                "invalid_move",
                "miss",
                "hit",
                "sunk_carrier",
                "sunk_battleship",
                "sunk_cruiser",
                "sunk_submarine",
                "sunk_destroyer"
            ]
        },
        "gameState": {
            "type": "string",
            "enum": [
                "lost",
                "in_progress",
                "won"
            ]
        },
        "opponentMoved": {
            "type": "bool"
        },
        "opponentMove": {
            "type": "object",
            "requred": false,
            "properties": {
                "index": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 99
                },
                "moveResult": {
                    "type": "string",
                    "enum": [
                        "miss",
                        "hit",
                        "sunk_carrier",
                        "sunk_battleship",
                        "sunk_cruiser",
                        "sunk_submarine",
                        "sunk_destroyer"
                    ]
                }
            }
        },
        "if": {
            "properties": { "opponentMoved": { "const": false } }
        },
        "then": {
            "properties": { "opponentMove": { "requred": false } }
        }
    }
}
```

### [new_game_request_schima.json](./json_schimas/new_game_request_schima.json)
```JSON
{
    "$schema": "http://json-schema.org/draft/2019-09/schema#",
    "definitions": {
        "ship": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 99
                },
                "isVertical": {
                    "type": "boolean"
                }
            }
        }
    },
    
    "type": "object",
    "properties": {
        "carrier": { "$ref": "#/definitions/ship" },
        "battleship": { "$ref": "#/definitions/ship" },
        "cruiser": { "$ref": "#/definitions/ship" },
        "submarine": { "$ref": "#/definitions/ship" },
        "destroyer": { "$ref": "#/definitions/ship" }
    }
}
```
