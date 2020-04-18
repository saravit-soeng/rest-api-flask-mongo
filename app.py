from flask import Flask
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.secret_key = "abc=="
app.config["MONGO_URI"] = "mongodb://localhost:27017/demo_db"
mongo = PyMongo(app)

swagger_url = "/api-docs"
api_url = "http://localhost:5000/"

swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url,
    config={
        'app_name':"Rest API with Flask and MongoDB"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=swaggerui_blueprint)