from flask import jsonify, make_response, request, current_app as app
from random import Random
from ..models.game_state_model import GameStateModel
from ..services.json import validate, NEW_GAME_REQUEST_SCHEMA
from ..services.battleship_ai import generateShips
from .. import db

r = Random()

@app.route('/battleship', methods=['GET'])
def battleship_game_state(): 
    user_id = request.cookies.get("battleship_user_id")
    game = GameStateModel.query.get(user_id)

    if game is None:
        return make_response("No game found!", 404)  # Not Found

    return make_response(jsonify(game.getState()), 200)  # Ok


@app.route('/battleship', methods=['PUT'])
def battleship_game_new(): 
    # Get user id for later
    user_id = request.cookies.get("battleship_user_id")
    if user_id is None:
        user_id = hex(r.randint(0x1000000000000000, 0xffffffffffffffff))[2:]

    # Get & validate JSON
    request_json = request.get_json()
    try:
        validate(request_json, NEW_GAME_REQUEST_SCHEMA)
    except:
        return make_response("JSON arguments invalid or missing!", 400)  # Bad Request

    # Make new game
    new_game = GameStateModel.newGame(request_json, generateShips())
    new_game.user_id = user_id
    old_game = GameStateModel.query.get(user_id)
    if old_game is not None:
        db.session.delete(old_game)
    db.session.add(new_game)
    db.session.commit()

    # Create response
    response = make_response("OK", 200)  # Ok
    response.set_cookie("battleship_user_id", user_id)
    return response

@app.route('/battleship/move/<index>', methods=['PUSH'])
def battleship_game_move(index): 
    pass
