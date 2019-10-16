from app.main import bp
from flask import render_template


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("calender.html")

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")
