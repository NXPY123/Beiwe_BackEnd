from flask import Blueprint, render_template, redirect, url_for, request,flash
from numpy import block, insert
#from requests import session
#from sqlalchemy import false, true 
from werkzeug.security import generate_password_hash, check_password_hash
#from models import User
#from __init__ import db
#from flask_login import login_user, login_required, logout_user,current_user
from app import mongo_black_list_collection,mongo_user_labels,mongo_user #To query and perform CRUD operations on mongo collection
import json
import labels
from google.oauth2 import service_account
from google.cloud import vision_v1
import os
import string
import random
import csv

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
        

        if mongo_user.count_documents({"email":email}): # if a user is found, we want to redirect back to signup page so user can try again
            user_exists_response_json = json.dumps({'error':"User already exists",'status':"User not created"})
            return user_exists_response_json

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = {
            "email":email,
            "name":name,
            "password":generate_password_hash(password, method='sha256'),
            "session":"None"
        }
        mongo_user.insert_one(new_user)
        # add the new user to the database
       

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
        user = mongo_user.find_one({"email":email})

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not mongo_user.count_documents({"email":email}) or not check_password_hash(user['password'], password):
            not_logged_in_response_json = json.dumps({'status':"Not logged in",'error':"User credentials don't match"})
            return not_logged_in_response_json # if the user doesn't exist or password is wrong

        # if the above check passes, then we know the user has the right credentials
       
        session_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7)) #Add session key to database
        #user["session"] = session_key
        mongo_user.update_one({"email":email},{"$set":{"session":session_key}})
        logged_in_response_json = json.dumps({'status':"Logged in",'error':"None",'session_key':session_key})
        return logged_in_response_json
    
    except Exception as Err:

        not_logged_in_response_json = json.dumps({'status':"Not logged in",'error':'Err'})
        return not_logged_in_response_json # if the user doesn't exist or password is wrong





@extension.route('/extension/logout')
#@login_required

def extension_logout():
    
    logout_json_response = request.args.get('logout_data')
    logout_data = json.loads(logout_json_response)

    #Request Format:
    '''
    {

        "data":{
            "email":
            "session_key":        

        }


    }
    '''

    email = logout_data['data']['email']
    session_key = logout_data['data']['session_key']

    try:

        user = mongo_user.find_one({"email":email})

        if not user or not user['session'] == session_key:
            not_logged_out_response_json = json.dumps({'status':"Not logged out",'error':"User credentials don't match"})
            return not_logged_out_response_json # if the user doesn't exist or session key is wrong
        random_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7)) #Replace session_key with random string
        record = mongo_user.find_one_and_update({"email":email},{ '$set': { "session" : random_key} })
        logged_out_response_json = json.dumps({'status':"logged out",'error':"None"})
        return logged_out_response_json # if the user is logged out

    except Exception as Err:

        not_logged_out_response_json = json.dumps({'status':"Not logged out",'error':'Err'})
        return not_logged_out_response_json 






@extension.route('/extension/setlabel')
#@login_required

def set_label():

    labels_json_response = request.args.get('labels')
    labels_data = json.loads(labels_json_response)


    #Request JSON Format
    '''
    {

        "data":{
            "labels":[]
            "email":
            "session_key":
        }

    }
    '''
    labels_list = labels_data["data"]["labels"]
    email = labels_data["data"]["email"]
    session_key = labels_data["data"]["session_key"]

    try:
        user = mongo_user.find_one({"email":email})
        if user and user['session']==session_key:
            name = user['name']
            #email = user.email
            missing = []
            correct_labels = []
            with open('google_labels.csv', 'r') as fp:
                s = csv.reader(fp)
                s = list(s)
                for label in labels_list:
                    if [label+";"] not in s:
                        missing.append(label)
                    else:
                        label = label.lower()
                        correct_labels.append(label)
                        
            if(mongo_user_labels.count_documents({"email":email})):
                record = mongo_user_labels.find_one_and_update({"email":email},{ '$set': { "labels" : correct_labels} })
            else:
                insert_rec = {
                    "name":name,
                    "email":email,
                    "labels":correct_labels
                    
                }
                record = mongo_user_labels.insert_one(insert_rec)
            labels_json_response = json.dumps({"status":"labels updated/inserted","error":"None","wrong_label":missing})
            return labels_json_response
        else:
            labels_json_response = json.dumps({"status":"user not logged in","error":"Authentication Failed"})
            return labels_json_response
    except Exception as Err:
        error_json_response = json.dumps({"status":"Error","error":'Err'})
        return error_json_response




@extension.route('/extension/api_call', methods=['GET', 'POST'])
#@login_required

def get_blocked_img():
    images_json_response = request.get_json(force = True)
    print(images_json_response)
    images_data = images_json_response["images"]
    #images_data = json.loads(images_json_response)
    email = images_data["data"]["email"]
    session_key = images_data["data"]["session_key"]


    try:
        user = mongo_user.find_one({"email":email})
        if user and user['session'] == session_key:
            name = user['name']
            
        else:
            error_json_response = json.dumps({"status":"Image labels not returned","error":'Not logged in'})
            return error_json_response
    except Exception as Err:
        error_json_response = json.dumps({"status":"Image labels not returned","error":'Err'})
        return error_json_response        


    #Request JSON Format
    '''
    {
        "data":{
            "img_urls":[]
            "email":
            "session_key":
            "website":
        }
    }
    
    '''
    img_url_list = images_data["data"]["img_urls"]
    user_labels = mongo_user_labels.find_one({"email":email})
    website = images_data["data"]["website"]
    blocked_imgs = []
    user_labels["labels"] = [label.lower() for label in user_labels["labels"]]
    for label in user_labels["labels"]:
        black_list_document = mongo_black_list_collection.find_one({"website":website,"label":label})
        if(black_list_document):
            blocked_imgs.extend(black_list_document["img_urls"])
            img_url_list = [x for x in img_url_list if x not in blocked_imgs]
        
    tag_list = [labels.label(i,client) for i in img_url_list]

    

    labels_list = [elem['tags'] for elem in tag_list]
    
    
    
   
    for index,img_list in enumerate(labels_list):
        for label in img_list:
            # print(label)
            if label.lower() in user_labels["labels"]:
                # print(labels_list.index(img_list))
                if (mongo_black_list_collection.count_documents({"website":website,"label":label})):
                   black_list_document = mongo_black_list_collection.find_one({"website":website,"label":label})
                   img_urls = black_list_document["img_urls"]
                   img_urls.append(img_url_list[index])
                   record = mongo_black_list_collection.find_one_and_update({"website":website,"label":label},{ '$set': { "img_urls" : img_urls} })
                else:
                   img_list = [img_url_list[index]]
                   rec = {
                       "label":label,
                       "website":website,
                       "img_urls":img_list
                   }
                   mongo_black_list_collection.insert_one(rec)
                   
                blocked_imgs.append(img_url_list[index]) # If Image is to be blocked, append it

                
                
    blocked_imgs = list(set(blocked_imgs)) #Remove duplicates
    print(blocked_imgs)
    labels_json_response = json.dumps({"blocked_images":blocked_imgs,"error":"None"})
    return labels_json_response
    



    #json_response = json.dumps({'labels':labels_list,'error':'None'})
    #return json_response



    
    '''
    mongo_user:

    {
        "email":
        "name":
        "password":
        "session":
    }
    
    '''



        
        




