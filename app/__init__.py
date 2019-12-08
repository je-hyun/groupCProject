from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models import User

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    #from app.models import db
    # Build the database every time "flask run" is executed.
    with app.test_request_context():
        db.create_all()
        if db.session.query(User).get(0) is None:
            print("No user found, creating a default user...")
            default_user = User(id=0, firstname="Je Hyun", lastname="Kim")
            db.session.add(default_user)
            db.session.commit()

    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app

from app import models
