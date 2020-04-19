from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='')
app.secret_key = "abc=="
# Mark: - for windows
# app.config["MONGO_URI"] = "mongodb://localhost:27017/demo_db"
# Mark: - for MacOS
app.config["MONGO_URI"] = "mongodb://saravit:1234@127.0.0.1:27017/demoDB"
mongo = PyMongo(app)
