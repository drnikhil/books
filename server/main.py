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

    migrate = Migrate(app, db, render_batch=True)
    
    CORS(app, resources={r'/*': {'origins': '*'}})

    with app.app_context():
        db.create_all()

    return app

from application.resource import *

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)