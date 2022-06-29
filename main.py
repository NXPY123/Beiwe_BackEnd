
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
from .labels import label


from flask_sqlalchemy import SQLAlchemy
from flask import render_template,Blueprint
from flask_login import login_required, current_user


from .models import User


credentials = service_account.Credentials.from_service_account_file('./config/beive-354409-0e474f6066a3.json')
client = vision_v1.ImageAnnotatorClient(credentials=credentials)

db = SQLAlchemy() 



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

