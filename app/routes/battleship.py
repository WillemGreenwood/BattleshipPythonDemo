from flask import current_app as app

@app.route('/battleship', methods=['GET'])
def battleship_game_state(): 
    pass

@app.route('/battleship', methods=['PUT'])
def battleship_game_new(): 
    pass

@app.route('/battleship/move/<index>', methods=['PUSH'])
def battleship_game_move(index): 
    pass
