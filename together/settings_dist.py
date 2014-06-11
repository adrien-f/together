import os


class Config(object):
    SECRET_KEY = ''  # Set it for cookies
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(object):
    SQLALCHEMY_ECHO = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://together:together@together.dev/together'
    SQLALCHEMY_ECHO = True
    YOUTUBE_API = ''
