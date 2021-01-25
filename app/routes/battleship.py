from flask import jsonify, make_response, request, current_app as app
from random import Random
from ..models.game_state_model import GameStateModel
from ..services.json import validate, NEW_GAME_REQUEST_SCHEMA
from ..services.battleship_ai import generateShips, move
from .. import db

r = Random()
win_state_map = {
    "player_one_victory": "won",
    "player_two_victory": "lost",
    "in_progress": "in_progress"
}

@app.route('/battleship', methods=['GET'])
def battleship_game_state(): 
    user_id = request.cookies.get("battleship_user_id")
    game = GameStateModel.query.get(user_id)

    if game is None:
        return make_response("No game found!", 404)  # Not Found

    state = game.getState()
    state["gameState"] = win_state_map[game.getWinState()]
    return jsonify(state)


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
    index = int(index)
    user_id = request.cookies.get("battleship_user_id")
    game = GameStateModel.query.get(user_id)

    if game is None:
        return make_response("No game found!", 404)  # Not Found

    player_move_result = game.move_player_one(index)
    move_result = {
        "index": index,
        "moveResult": player_move_result,
        "opponentMoved": False
    }

    if player_move_result != "invalid_move" and game.getWinState() != "player_one_victory":
        ai_index, ai_move_result = move(game)
        move_result["opponentMoved"] = True
        move_result["opponentMove"] = {
                "index": ai_index,
                "moveResult": ai_move_result
            }
    
    move_result["gameState"] = win_state_map[game.getWinState()]
    
    db.session.commit()
    return make_response(jsonify(move_result), 200)  # Ok
