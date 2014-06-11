from flask import Flask, url_for, redirect
from flask_wtf import CsrfProtect
import os


def create_app():
    app = Flask(__name__, static_folder='public')

    CsrfProtect(app)

    env = os.environ.get('TOGETHER_ENV', 'dev')
    app.config.from_object('together.settings.{}Config'.format(env.capitalize()))
    app.config['ENV'] = env

    from together.models import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from together.meta import meta
    app.register_blueprint(meta, url_prefix='/')

    from together.api import api, json_user
    api.init_app(app)

    app.context_processor(json_user)

    from together.assets import assets_env
    assets_env.init_app(app)

    return app
