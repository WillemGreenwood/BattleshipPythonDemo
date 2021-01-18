import json
import jsonschema

def readJsonFromFile(filename):
    contents = None
    with open(filename, "r") as file:
        contents = json.load(file)
    return contents

def validate(instance, schema):
    return jsonschema.validate(instance=instance, schema=schema)

GAME_STATE_SCHEMA = readJsonFromFile("json_schemas/game_state_schema.json")
MOVE_RESPONSE_SCHEMA = readJsonFromFile("json_schemas/move_response_schema.json")
NEW_GAME_REQUEST_SCHEMA = readJsonFromFile("json_schemas/new_game_request_schema.json")
