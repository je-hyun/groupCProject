#### Itinerary app.
A personalized event recommendation website which accommodates to your schedule and preferences.

#### Basic folder structure.
- `app` : folder you implement your Flask project.
- `app.py`: In the main file that starts your sample project.
- `tests`: Here you need to include all unit and functional test for your project.
- `project_management` : In this folder you are expected to store all project documentation, and project deliverables associated with the course.


#### Run Instructions

```shell
git clone https://github.com/je-hyun/groupCProject.git
cd groupCProject
```

The project uses `pipenv` virtual environment. Make sure you install `pipenv` on your machine. Enter the virtual enviroment py typing:

```shell
pipenv shell
```

Once your virtual environment is activated,
```shell
pip install flask
pip install flask_sqlalchemy
pip install Flask-WTF
pip install geopy
pip install flask-migrate
flask run
```

You may need to specify the flask app name running the command.
```shell  
 export FLASK_APP=app.py
```

#### Changing models.py
If you are adding to the project, you may find you want to change the database schema. If so, a database migration will be necessary. After you change the models.py file, you can run the following commands inside the project root directory to migrate the database.
```
flask db migrate -m "your description of changes"
flask db upgrade
```

If, for any reason during development, you need to downgrade to a previous version of the database, simply use this command.
```
flask db downgrade
```
