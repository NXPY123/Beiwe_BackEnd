from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request
import io
import os
import requests
import json
# Imports the Google Cloud client library
from google.cloud import vision_v1
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.cloud.vision import AnnotateFileRequest
import proto
from labels import label
from models import User
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import pymongo
from flask_cors import CORS

db = SQLAlchemy() #Instance of SQAlchemy (Object Relational Mapper)
migrate = Migrate() #Instance of Migrations 

ENV = 'prod'

credentials = service_account.Credentials.from_service_account_file(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
client = vision_v1.ImageAnnotatorClient(credentials=credentials)
load_dotenv() # use dotenv to hide sensitive credential as environment variables. load_dotenv() is a function that loads the .env file into the environment

def create_app():
    app = Flask(__name__)
    CORS(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

   
    
    app.config['SECRET_KEY'] = '2bbe896fe65d7214473d25bbf85b817ee9103d491d1f964a'  #Secret Key to encrypty cookies to send to browsers
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #Configure Database URI
    if ENV == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://upilzfdcnzbtsj:7181a85cdb0a5be27b7d8377c04652b5e92e5fc0cde15897d97294ebf1e0058f@ec2-3-224-8-189.compute-1.amazonaws.com:5432/d27dj586047kr2'

   
    
    
    db.init_app(app) #Instantiate Database with App
    migrate.init_app(app, db) #Inintailize migrations

    

   
   
    #Register auth blueprint
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Register main blueprint
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #Register extension blueprint
    from extension import extension as extension_blueprint
    app.register_blueprint(extension_blueprint)

    return app


