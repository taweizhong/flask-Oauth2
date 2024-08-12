import os
from .model import db
from .routes import bp
from .oauth2 import config_oauth
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    # load default configuration
    app.config.from_object('website.settings')
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

    # load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    sut_up(app)
    return app


def sut_up(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    config_oauth(app)
    app.register_blueprint(bp, url_prefix="")