from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

def create_app():
    app = Flask(__name__, template_folder="templates")
    from app.models import db
    app.config.from_object(Config)
    login.init_app(app)

    # Build the database every time "flask run" is executed.
    with app.test_request_context():
        db.init_app(app)
        db.create_all()

    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app
