from app.main import bp


@bp.route('/', methods=['GET','POST'])
def index():
    return "This is a basic route."
