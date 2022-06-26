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

app = Flask(__name__)


credentials = service_account.Credentials.from_service_account_file('./google_vision_api/config/beive-354409-0e474f6066a3.json')
image = vision_v1.types.Image()
client = vision_v1.ImageAnnotatorClient(credentials=credentials)




@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/website',endpoint = 'label', methods=['GET', 'POST'])
def label():

    img_uri = request.args.get('params') 
   
   
    image.source.image_uri = img_uri
    response = client.label_detection(image=image)
    

    #response = MessageToJson(response, preserving_proto_field_name = True)
    #desired_res 
    #labels = response.label_annotations
    
    serializable_tags = [proto.Message.to_dict(tag) for tag in response.label_annotations]
    
    print(serializable_tags)
    
    return {'serial':serializable_tags}
    #return render_template('image_label.html',labels=labels)





