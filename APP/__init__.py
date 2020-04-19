from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from APP.config import Config
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

#Registers#
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # inits #
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    #Import routes#
    from APP.main.routes import main
    from APP.logApp.routes import logApp
    from APP.users.routes import users
    from APP.errors.handlers import errors

    # Register Blueprints #
    app.register_blueprint(main)
    app.register_blueprint(logApp)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app




