from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Build the database every time "flask run" is executed.
    with app.test_request_context():
        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'login'
        '''
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        '''
        db.create_all()

    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app
