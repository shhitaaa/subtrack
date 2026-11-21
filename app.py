import os
from flask import Flask
from dotenv import load_dotenv
from iterations.sprint1 import bp as sprint1_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
    app.register_blueprint(sprint1_bp)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
