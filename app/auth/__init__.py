from flask import blueprint

bp = Blueprint('auth',__name__)

from app.auth import routes
