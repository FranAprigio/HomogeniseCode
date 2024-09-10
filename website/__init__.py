from flask import Flask
from flask_login import LoginManager
from website.settings import db
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)   

    engine = db.get_engine()

    app.config['SECRET_KEY'] = '1234'    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5434/{os.getenv('POSTGRES_DB')}"
db = SQLAlchemy(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    db.set_audit_log()

    @login_manager.user_loader
    def load_user(id):

        session = db.get_dbsession()
        usersession = session.query(models.user)

        return usersession.get(int(id))

    return app