import sys
import os
sys.path.append(os.path.dirname(__file__))

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from jobby.config import Config
from flask_migrate import Migrate
from flask_socketio import SocketIO
from utils import dir_last_updated, mail

db = SQLAlchemy()
csrf = CSRFProtect()
socketio = SocketIO(cors_allowed_origins='*')
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'account.login'
login_manager.login_message = "Please login to see this page"
last_updated = dir_last_updated('jobby/static')

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate()

    db.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app,db)
        db.create_all()
    login_manager.init_app(app)

    from jobby.account.views import account
    from jobby.public.views import public
    from jobby.posttask.views import posttask
    from jobby.manage.views import manage
    from jobby.message.views import message
    from jobby.setting.views import setting
    from jobby.editProfile.views import editProfile
    app.register_blueprint(account)
    app.register_blueprint(public)
    app.register_blueprint(posttask)
    app.register_blueprint(manage)
    app.register_blueprint(message)
    app.register_blueprint(setting)
    app.register_blueprint(editProfile)

    return app
