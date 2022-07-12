from flask import Blueprint, render_template, redirect, url_for, request,flash
from numpy import insert
from sqlalchemy import false, true 
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from __init__ import db
from flask_login import login_user, login_required, logout_user,current_user
from app import mongo_black_list_collection,mongo_user_labels #To query and perform CRUD operations on mongo collection
import json
import labels
from google.oauth2 import service_account
from google.cloud import vision_v1
import os

extension = Blueprint('extension', __name__)


credentials = service_account.Credentials.from_service_account_file(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
client = vision_v1.ImageAnnotatorClient(credentials=credentials)


@extension.route('/extension/signup', methods=['GET', 'POST'])
def extension_signup():
    signup_json_response = request.args.get('signup_data')
    signup_data = json.loads(signup_json_response)

    #Request Format:
    '''
    {
        "data":{
            "email":
            "name":
            "password":

            }
    }
    '''
    email = signup_data['data']['email']
    name = signup_data['data']['name']
    password = signup_data['data']['password']

    try:
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            user_exists_response_json = json.dumps({'error':"User already exists",'status':"User not created"})
            return user_exists_response_json

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        user_created_response_json = json.dumps({'status':"User Created",'error':"None"})
        return user_created_response_json


    except Exception as Err:
        exception_response_json = json.dumps({'error':Err,'status':"User not created"}) 
        return exception_response_json





@extension.route('/extension/login', methods=['GET', 'POST'])

def extension_login():

    login_json_response = request.args.get('login_data')
    login_data = json.loads(login_json_response)

    #Request Format:
    '''
    {

        "data":{
            "email":
            "password":        

        }


    }
    '''

    email = login_data['data']['email']
    password = login_data['data']['password']
    remember = True 

    try:
        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            not_logged_in_response_json = json.dumps({'status':"Not logged in",'error':"User credentials don't match"})
            return not_logged_in_response_json # if the user doesn't exist or password is wrong

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        logged_in_response_json = json.dumps({'status':"Logged in",'error':"None"})
        return logged_in_response_json
    
    except Exception as Err:

        not_logged_in_response_json = json.dumps({'status':"Not logged in",'error':Err})
        return not_logged_in_response_json # if the user doesn't exist or password is wrong



@extension.route('/extension/logout')
@login_required

def extension_logout():
    logout_user()



@extension.route('/extension/setlabel')


def set_label():

    labels_json_response = request.args.get('labels')
    labels_data = json.loads(labels_json_response)


    #Request JSON Format
    '''
    {

        "data":{
            "labels":[]
        }

    }
    '''
    labels_list = labels_data["data"]["labels"]

    try:
        if current_user.is_authenticated:
            name = current_user.name
            email = current_user.email
            if(mongo_user_labels.count_documents({"email":email})):
                record = mongo_user_labels.find_one_and_update(filter={"email":email},update={ '$set': { "labels" : labels_list} })
            else:
                insert_rec = {
                    "name":name,
                    "email":email,
                    "labels":labels_list
                    
                }
                record = mongo_user_labels.insert_one(insert_rec)
            labels_json_response = json.dumps({"status":"labels updated/inserted","error":"None"})
            return labels_json_response
        else:
            labels_json_response = json.dumps({"status":"user not logged in","error":"Authentication Failed"})
            return labels_json_response
    except Exception as Err:
        error_json_response = json.dumps({"status":"Error","error":Err})
        return error_json_response




@extension.route('/api_call', methods=['GET', 'POST'])
@login_required

def get_blocked_img():
    images_json_response = request.args.get('images')
    images_data = json.loads(images_json_response)

    try:
        if current_user.is_authenticated():
            name = current_user.name
            email = current_user.email
        else:
            error_json_response = json.dumps({"status":"Image labels not returned","error":'Not logged in'})
            return error_json_response
    except Exception as Err:
        error_json_response = json.dumps({"status":"Image labels not returned","error":Err})
        return error_json_response        


    #Request JSON Format
    '''
    {
        "data":{
            "img_urls":[]
        }
    }
    
    '''
    img_url_list = images_data["data"]["img_urls"]

    json_list = [labels.label(i,client) for i in img_url_list]

    

    labels_list = [descr['tags'] for descr in json_list]
    user_labels = mongo_user_labels.find_one(query={"email":email},projection={"labels"})
    
    
  
    for image in labels_list:
        for label in image:
            if(label in user_labels["labels"] ):
                image = true # If Image is to be blocked, replace it with true
                break
        if(image != true): 
            image = false # If image shouldn't be blocked

    labels_json_response = json.dumps({"blocked_images":labels_list,"error":"None"})
    return labels_json_response
    



    #json_response = json.dumps({'labels':labels_list,'error':'None'})
    #return json_response



    



        
        




