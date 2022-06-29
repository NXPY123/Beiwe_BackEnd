
from .__init__ import db
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
import proto
from .labels import label
from .__init__ import client as client
from flask import render_template,Blueprint
from flask_login import login_required, current_user


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