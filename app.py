import os
from os.path import join,dirname
from dotenv import load_dotenv

from flask import Flask,render_template,jsonify,request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('DB_NAME')

connection_String ='mongodb+srv://tes:sparta@cluster0.rdnnt7s.mongodb.net/?retryWrites=true&w=majority'
Client = MongoClient(connection_String)
db = Client.dbsparta


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary',methods=['GET'])
def show_diary():
   articles = list(db.diary.find({},{'_id':False}))
   return  jsonify({'articles':articles})

@app.route('/diary',methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    file = request.files['file_give']
    extention = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'static/post-{mytime}.{extention}'
    file.save(filename)

    profile = request.files['profile_give']
    profile_extention = profile.filename.split('.')[-1]
    profile_filename = f'static/profile-{mytime}.{profile_extention}'
    profile.save(profile_filename)

    time = today.strftime('%Y.%m.%d')


    doc = {
        'file': filename,
        'profile': profile_filename,
        'title':title_receive,
        'content':content_receive,
        'time': time,
    }

    db.diary.insert_one(doc)
    return jsonify ({'massage':'data was saved!!!'})


if __name__ == '__main__':
    app.run(port=5000,debug=True)