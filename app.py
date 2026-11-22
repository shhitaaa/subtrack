
import os
from flask import Flask
from dotenv import load_dotenv

from iterations.sprint1 import bp as sprint1_bp
from iterations.sprint2 import bp as sprint2_bp
from iterations.sprint3 import bp as sprint3_bp
from iterations.sprint4 import bp as sprint4_bp
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")

    # Register sprint blueprints
    app.register_blueprint(sprint1_bp)
    app.register_blueprint(sprint2_bp)
    app.register_blueprint(sprint3_bp)
    app.register_blueprint(sprint4_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
