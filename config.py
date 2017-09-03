import os
import random, string

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class LocalConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../local.db'
    BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT =  587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['MAIL_USERNAME'] # 'igorppsan@gmail.com'
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD'] # 'macacovelhoeikebatista'
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER'] # 'flask@example.com'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    # BROKER_URL = os.environ['REDIS_URL']
    # CELERY_RESULT_BACKEND = os.environ['REDIS_URL']


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    # BROKER_URL = os.environ['REDIS_URL']
    # CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
