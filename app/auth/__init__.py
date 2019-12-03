from flask import Blueprint
from app.auth import routes

bp = Blueprint('auth', __name__, template_folder='app/templates')
#bp.debug = True
#bp.run()

if __name__ == '__main__':
    bp.debug = True
    bp.run(debug=True)