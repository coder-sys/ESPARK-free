from flask import Flask,after_this_request
import time

from youtubesearchpython import VideosSearch

from googlesearch import search

from bs4 import BeautifulSoup
import requests

def get_google_data(query):
    array = []
    array_urls = []
    i= 0
    for url in search(query,12):
        print (url)
        array_urls.append(url)
        data = requests.get(url)
        soup = BeautifulSoup(data.text,'html.parser')
        for _ in soup.find_all('title'):
            print(_.get_text())
            array.append(_.get_text())
        if len(array) > 29:   
            break
    return [array,array_urls]

app = Flask(__name__)

firebaseConfig = {
  'apiKey': "AIzaSyCGvp-4gW3nC3fAHmnJDAx3Fbwsdzn_LRQ",
  'authDomain': "espark-356318.firebaseapp.com",
  'databaseURL': "https://espark-356318-default-rtdb.firebaseio.com",
  'projectId': "espark-356318",
  'storageBucket': "espark-356318.appspot.com",
  'messagingSenderId': "615921346526",
  'appId': "1:615921346526:web:6a37c444f53906c90c9f4f"
}
import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("espark-a18da-firebase-adminsdk-s233j-0ad1627f54.json")
firebase_admin.initialize_app(cred)
fd = firestore.client()
fd.collection('data').document('info').set({'data':1})
@app.route('/sign_in/<input_name>/<input_name_0>/<password>/<email>',methods=['GET'])
def sign_in(input_name,input_name_0,password,email):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    lastname = input_name_0
    password = password
    email = email
    db.child(f'Users/{input_name}').set({
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email,
        'no_of_folders':0
    })
    return {
        'firstname':input_name,
        'lastname':lastname,
        'password':password,
        'email':email
    }

@app.route('/login/<first_name>',methods=['GET'])
def login(first_name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        referance = db.child(f'Users/{first_name}').get()
        print(dict(referance.val())['password'])
        return {"data":dict(referance.val())['password']}
    except:
        return {"data":"username not found"}
@app.route('/add_folder/<name>/<foldername>',methods=['GET'])
def add_folder(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        fd.collection(name).document(foldername).set({'foldername':foldername})
        return {'data':'doable'}

    except:
        print('cannot do so')    
        return {'data':"undoable"}
@app.route('/add_folder/<name>',methods=['GET'])
def update_no_of_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    no_of_folders = db.child(f'Users/{name}/no_of_folders').get().val()
    db.child(f'Users/{name}').update({
        'no_of_folders':no_of_folders+1
    })
    return {'data':200,'no_of_folders':no_of_folders}
@app.route('/get_folders/<name>')
def get_folders(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    try:
        d = fd.collection(name).get()
        print(d)
        data = []
        for _ in d:
            print("The value im looking for : ")

            print(_.to_dict())
            data.append(_.to_dict()['foldername'])
        return {'data':data}

    except:
        print('cannot do so')    
        return {'data':"undoable"}


@app.route('/get_google_content/<query>',methods=['GET'])
def get_google_content(query):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    x,y = get_google_data(query)
    return{'names':x,'urls':y}
@app.route('/add_google_content/<name>/<foldername>/<sourcename>/<sourcepath>',methods=['GET'])
def add_google_content(name,foldername,sourcename,sourcepath):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").add({'link':sourcepath,'name':sourcename})
    time.sleep(3)
    
    return{"status":sourcepath}
@app.route('/add_youtube_content/<name>/<foldername>/<sourcename>/<sourcepath>',methods=['GET'])
def add_youtube_content(name,foldername,sourcename,sourcepath):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    fd.collection(name).document(foldername).collection("content_stored").add({'link':'https:__www.youtube.com_watch?v='+sourcepath,'name':sourcename})
    
    return{"status":sourcepath}
@app.route('/get_youtube_data/<query>',methods=['GET'])
def get_youtube_data(query):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    videosSearch = VideosSearch(query, limit = 20).result()

    videosSearch = videosSearch['result']
    titlearray=[]
    thumbnailarray = []
    linkarray = []

    for i in videosSearch:
        print(i)
        titlearray.append(i['title'])
        thumbnailarray.append(i['thumbnails'])
        linkarray.append(i['link'])
    return{
    'titles':titlearray,
    'thumbnail':thumbnailarray,
    'link':linkarray,
    'length':len(titlearray)==len(thumbnailarray)==len(linkarray)
    }
@app.route("/load_data/<name>/<foldername>",methods=['GET'])
def load_data(name,foldername):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    stored_data = fd.collection(name).document(foldername).collection('content_stored').get()
    stored_data = list(stored_data)
    array = []
    for _ in stored_data:
        array.append(_.to_dict())
    print(stored_data)

    return{'data':array}
@app.route('/get_last_name_and_email/<name>',methods=['GET'])
def get_last_name_and_email(name):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    stored_data = db.child(f'Users/{name}/email').get().val()
    stored_data1 = db.child(f"Users/{name}/lastname").get().val()
    return {
        'email':stored_data,
        'lastname':stored_data1
    }
@app.route('/verify_sign_in_information/<name>/<lname>',methods=['GET'])
def verify_sign_in_information(name,lname):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = db.child('Users/').get().val()
    resp = '-'
    if data:
        for i in data:
            if (data[i]['lastname']+data[i]['firstname']) == (lname+name):
                resp = 'change either of the names to continue'
                break
            else:
                resp = 'good to go!'
        
        return {
      'data':resp,
      'info':data
    }
    if not data:
        return{
            'data':'good to go!',
            'info':data,
            'status':200
        }
if __name__=='__main__':
    app.run(debug=True,host="localhost",port=8000)
