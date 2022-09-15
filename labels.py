from flask import Flask,request
import io
import os
import requests
import json
# Imports the Google Cloud client library
from google.cloud import vision_v1
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToDict
from google.cloud.vision import AnnotateFileRequest
import proto



def label(img_uri,client):

    

    image = vision_v1.types.Image() #Image Object
    print("img_uri passed: ")
    print(img_uri)
    image.source.image_uri = img_uri #To get image from img_link
    response = client.label_detection(image=image) #Detect Labels
    print("response: ")
    print(response)
    
    
   
    
    serializable_tags = [proto.Message.to_dict(tag) for tag in response.label_annotations] #Convert object to list type
    print("labels for each image")
    print(serializable_tags)
    tags_list = [i['description'] for i in serializable_tags] #Get only description from list
    print("tags list :")
    print(tags_list)
    return {'tags':tags_list}
    
    
