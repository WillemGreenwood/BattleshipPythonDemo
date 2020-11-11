from flask import Flask

def create_app():
    """Construct the Battleship application."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        from .routes import battleship

    return app
