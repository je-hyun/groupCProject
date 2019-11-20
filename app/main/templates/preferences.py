from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class Preferences(Form)-
    budget = TextField('Budget:', validators=[validators.required()])
    location = TextField('Location:', validators=[validators.required(), validators.Length(min=6, max=35)])
    distance = TextField('Distance willing to travel (in miles):', validators=[validators.required(), validators.Length(min=3, max=35)])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = Preferences(request.form)

        print form.errors
        if request.method == 'POST':
            budget = request.form['budget']
            location = request.form['location']
            distance = request.form['distance']
            print budget, " ", location, " ", distance

        if form.validate():
            # Save the comment here.
            flash('Thanks for registering your preferences ' + name)
        else:
            flash('Error: All the form fields are required. ')

        return render_template('hello.html', form=form)


if __budget__ == "__main__":
    app.run()


    @app.route('/', methods=['GET', 'POST'])
    def get_data():
        if request.method == 'POST':
            budget = request.form['budget']
            location = request.form['location']
            distance = request.form['distance']
            connection = mysql.get_db()
            cursor = connection.cursor()
            query = "INSERT INTO names_tbl(budget,location,distance) VALUES(%s,%s,%s)"
            cursor.execute(query, (budget, location, distance))
            connection.commit()


    return render_template('preferences.html')

    if __name__ == '__main__':
        app.run(debug=True