from flask import Flask, current_app


def create_app():
    app = Flask(__name__, template_folder="templates")

    #
    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app;
