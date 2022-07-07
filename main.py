
#from .__init__ import db
from flask import Flask,request,Blueprint
import io
import os
import requests
import json
# Imports the Google Cloud client library
from google.cloud import vision_v1
#from google.oauth2 import servicefrom project 
#import db, create_app, models_account
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.cloud.vision import AnnotateFileRequest
from google.oauth2 import service_account
import proto
from labels import label


from flask_sqlalchemy import SQLAlchemy
from flask import render_template,Blueprint
from flask_login import login_required, current_user


from models import User
import pymongo

credentials = service_account.Credentials.from_service_account_file('./config/beive-354409-0e474f6066a3.json')
client = vision_v1.ImageAnnotatorClient(credentials=credentials)

db = SQLAlchemy() 

MONGO_CONNECTION_STRING = f'mongodb+srv://NXPY123:{os.environ.get("password")}@mongo-beiwei-cluster-mu.7f9ix.mongodb.net/?retryWrites=true&w=majority'
mongo_client=pymongo.MongoClient(MONGO_CONNECTION_STRING) #Establish connection
mongo_db=mongo_client.Beiwei # assign database to mongo_db
mongo_black_list_collection = mongo_db.image_black_list

emp_rec1 = {
        "name":"Mr.Geek",
        "eid":24,
        "location":"delhi"
        }
rec_id1 = mongo_black_list_collection.insert_one(emp_rec1)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    
    return render_template('profile.html',name=current_user.name)


@main.route('/website',endpoint = 'label', methods=['GET', 'POST'])
@login_required
def web_request():

    img_uri = request.args.get('params') 

    response = label(img_uri,client) #Get response as dict
    return response

