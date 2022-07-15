'''from flask import Flask,request
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

app = Flask(__name__)


credentials = service_account.Credentials.from_service_account_file('./config/beive-354409-0e474f6066a3.json')

client = vision_v1.ImageAnnotatorClient(credentials=credentials)




@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/website',endpoint = 'label', methods=['GET', 'POST'])
def web_request():

    img_uri = request.args.get('params') 

    response = label(img_uri,client) #Get response as dict
    return response
    
    
    
    #return render_template('image_label.html',labels=labels)



'''
# IMPORTANT: Set environment variable mongo_password to access mongodb
from __init__ import create_app
#from flask_sqlalchemy import SQLAlchemy
from models import *
import pymongo
import os

MONGO_CONNECTION_STRING = f'mongodb+srv://NXPY123:{os.environ.get("mongo_password")}@mongo-beiwei-cluster-mu.7f9ix.mongodb.net/?retryWrites=true&w=majority'
mongo_client=pymongo.MongoClient(MONGO_CONNECTION_STRING) #Establish connection
mongo_db=mongo_client.Beiwei # assign database to mongo_db
mongo_black_list_collection = mongo_db.image_black_list #To perform operations on collection
mongo_user_labels = mongo_db.user_labels
mongo_user = mongo_db.user
app = create_app()
#db = SQLAlchemy(app)
