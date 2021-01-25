from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the Battleship application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # models
        from .models.game_state_model import GameStateModel
        db.create_all()

        # routes
        from .routes import battleship
        from .routes import battleship_ui

    return app
