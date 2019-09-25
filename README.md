#### CUS Project Template.
This repository serves as a starting point for your project. It is organize  in a way to allows the monitoring of project deliverables.

#### Basic folder structure.
- `app` : folder you implement your Flask project.
- `app.py`: In the main file that starts your sample project.
- `tests`: Here you need to include all unit and functional test for your project.
- `project_management` : In this folder you are expected to store all project documentation, and project deliverables associated with the course.

#### Basic Flask application.

A basic flask application is provided for you. The project uses `pipenv` virtual environment. Make sure you install `pipenv` on your machine.

Enter the virtual enviroment py typing

```shell
pipenv shell
```
You might need to specify the flask app name running the command.
```shell  
 export FLASK_APP=app.py
```
You can start the basic application by issuing the command.

```shell
flask run
```
