from flask import Flask, current_app, app
from config import Config
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__, template_folder="templates")
    from app.models import db
    app.config.from_object(Config)

    # Build the database every time "flask run" is executed.
    with app.test_request_context():
        db.init_app(app)
        db.create_all()

    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app

# EMAIL SETTINGS.
MAIL_SERVER='smtp.gmail.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME = 'your@gmail.com',
MAIL_PASSWORD = 'yourpassword',
mail = Mail(app)

@app.route('/send-mail/')
def send_mail():
	try:
		msg = Message("Send Email",
		  sender="sendingemail@gmail.com",
		  recipients=["recievingemail@email.com"])
		msg.body = "Email Body"
		mail.send(msg)
		return 'Message sent!'
	except Exception as e:
		return(str(e))