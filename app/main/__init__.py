from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')
auth = Blueprint('auth', __name__, template_folder='tempaltes')


from app.main import routes
#bp.config['DEBUG'] = True