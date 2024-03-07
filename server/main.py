from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager   
from config import DevelopmentConfig
from application.models import db, bcrypt
from flask_migrate import Migrate
from application.resource import api
############################################
from celery.schedules import crontab
import flask_excel as excel
from celery import Celery
from application.tasks import daily_reminder
from application.instances import cache



jwt = JWTManager()  

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-secret-key')
    app.config['UPLOAD_FOLDER'] = 'uploads'  

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    excel.init_excel(app)
    cache.init_app(app)

    migrate = Migrate(app, db, render_batch=True)
    
    CORS(app, resources={r'/*': {'origins': '*'}})

    with app.app_context():
        db.create_all()

    return app



from application.worker import celery_init_app
app = create_app()
celery_app= None
celery_app=celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=25, day_of_month=3),
        daily_reminder.s('kitabwalatasks@taskmaster','test'),
    )



from application.resource import *



if __name__ == '__main__':    
    app.run(debug=True)