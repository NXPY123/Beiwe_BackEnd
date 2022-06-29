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

from .__init__ import create_app
app = create_app()

