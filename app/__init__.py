from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///restaunt.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS" : False
    })

    db.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app