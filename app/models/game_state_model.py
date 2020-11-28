from .. import db
from ..game.game_state import Game

class GameStateModel(db.Model):
    """lorem ipsum"""

    __tablename__ = "gamestates"

    id = db.Column(
        "id",
        db.Integer,
        primary_key=True
    )

    sesskey = db.Column(
        "sesskey",
        db.Integer,
        index=True
    )

    player1Ships = db.Column(
        "player1ships",
        db.String(21)
    )

    player2Ships = db.Column(
        "player2ships",
        db.String(21)
    )

    gridState = db.Column(
        "gridstate",
        db.String(100)
    )

    lastUpdated = db.Column(
        "lastupdated",
        db.DateTime()
    )

    @classmethod
    def from_game_state(cls, game: Game) -> GameStateModel:
        model = GameStateModel()

        model.player1Ships = str(game.p1_ship_health["all"])
        for name, ship in game.p1_pieces:
            model.player1Ships += ("" if ship.index > 9 else "0")
            model.player1Ships += str(ship.index)
            model.player1Ships += ("v" if ship.isVertical else "h")
            model.player1Ships += str(game.p1_ship_health[name])

        model.player2Ships = str(game.p2_ship_health["all"])
        for name, ship in game.p2_pieces:
            model.player2Ships += ("" if ship.index > 9 else "0")
            model.player2Ships += str(ship.index)
            model.player2Ships += ("v" if ship.isVertical else "h")
            model.player2Ships += str(game.p2_ship_health[name])

        model.gridState = ""
        for p1,p2,_,_ in game.state_grid:
            model.gridState += str(p1 + (p2 << 1))

        return model
