from flask import Flask, render_template
from flask import redirect, url_for
#from flask_cors import CORS
from datetime import datetime, timedelta
#from celery import Celery
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import os

from celery import Celery

from .models import db
from .models.post import Post

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    # migrate = Migrate(app, db)
    # print(migrate)
    #print(dir(migrate))
    return app

def setup_database(app):
    with app.app_context():
        db.create_all()



# app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
# app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']

#CORS(app)


app = create_app()

celery = Celery(app.name, broker=app.config['BROKER_URL'])
celery.conf.update(app.config)


if not os.path.isfile('..local.db'):
    setup_database(app)


from blue.site.views import site_mod
#from blue.api.routes import mod

app.register_blueprint(site.views.site_mod, url_prefix='/site')
#app.register_blueprint(api.routes.mod, url_prefix='/api')

@app.route('/')
def index():
    return redirect(url_for('site.index'))

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
