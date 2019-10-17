from app.main import bp
from flask import Flask, render_template, request

from app.models import db, Users
from flask_sqlalchemy import SQLAlchemy

@bp.route('/', methods=['GET', 'POST'])
def index():
    #users = Users.query.all()
    users = db.session.query(Users).all()
    return render_template("calender.html", users=users)

@bp.route('/pref', methods=['GET', 'POST'])
def index2():
    return render_template("Preference.html")
