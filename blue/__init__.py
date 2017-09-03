from flask import Flask
#from flask_cors import CORS

#from celery import Celery

import os


from .models import db
from .models.post import Post

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    return app

def setup_database(app):
    with app.app_context():
        db.create_all()


# app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
# app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']

#CORS(app)

# celery = Celery(app.name, broker=app.config['BROKER_URL'])
# celery.conf.update(app.config)

app = create_app()

#if os.path.isfile('local.db'):
#    os.remove('local.db')
setup_database(app)


from blue.site.views import site_mod
#from blue.api.routes import mod

app.register_blueprint(site.views.site_mod, url_prefix='/site')
#app.register_blueprint(api.routes.mod, url_prefix='/api')
