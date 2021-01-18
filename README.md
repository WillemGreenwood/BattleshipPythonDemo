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
                "carrier": { "$ref": "#/definitions/ship", "required": true },
                "battleship": { "$ref": "#/definitions/ship", "required": true },
                "cruiser": { "$ref": "#/definitions/ship", "required": true },
                "submarine": { "$ref": "#/definitions/ship", "required": true },
                "destroyer": { "$ref": "#/definitions/ship", "required": true } 
            }
        },
        "ship": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "required": true,
                    "minimum": 0,
                    "maximum": 99
                },
                "isVertical": {
                    "type": "boolean",
                    "required": true
                }
            }
        }
    },

    "type": "object",
    "properties": {
        "gameState": {
            "type": "string",
            "required": true,
            "enum": [
                "lost",
                "in_progress",
                "won"
            ]
        },
        "playerShips": { "$ref": "#/definitions/ships", "required": true },
        "opponentShips": { "$ref": "#/definitions/ships", "required": true },
        "grid": {
            "type": "array",
            "required": true,
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
        "index": {
            "type": "integer",
            "required": true,
            "minimum": 0,
            "maximum": 99
        },
        "moveResult": {
            "type": "string",
            "required": true,
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
            "required": true,
            "enum": [
                "lost",
                "in_progress",
                "won"
            ]
        },
        "opponentMoved": {
            "type": "boolean",
            "required": true
        },
        "opponentMove": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "required": true,
                    "minimum": 0,
                    "maximum": 99
                },
                "moveResult": {
                    "type": "string",
                    "required": true,
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
        }
    },
    "if": {
        "properties": { "opponentMoved": { "const": true } }
    },
    "then": {
        "required": ["opponentMove"]
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
                    "maximum": 99,
                    "required": true
                },
                "isVertical": {
                    "type": "boolean",
                    "required": true
                }
            }
        }
    },
    
    "type": "object",
    "properties": {
        "carrier": { "$ref": "#/definitions/ship", "required": true },
        "battleship": { "$ref": "#/definitions/ship", "required": true },
        "cruiser": { "$ref": "#/definitions/ship", "required": true },
        "submarine": { "$ref": "#/definitions/ship", "required": true },
        "destroyer": { "$ref": "#/definitions/ship", "required": true }
    }
}
```
