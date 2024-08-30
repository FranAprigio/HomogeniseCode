from flask import Flask
from flask_login import LoginManager

from website.settings.db import database_init

def create_app():
    app = Flask(__name__)   
    app.config.from_object("config")

    from .settings.db import db

    app.config['SECRET_KEY'] = '1234'
    db.init_app(app)

    try:
        database_init(app)
    except Exception as e:
        app.logger.critical(f"Could not connect to postgres: {str(e)}")

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # type: ignore
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):

        session = db.get_dbsession()
        usersession = session.query(models.user)

        return usersession.get(int(id))

    return app
