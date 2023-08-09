from flask import Flask, Response, request,flash, render_template, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from datetime import datetime
import math
import requests

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup


app = Flask(__name__, static_folder="assets", template_folder="templates")
CORS(app)




    
 
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


 
@app.route('/add', methods=['GET','POST'])
def add_date():
    return render_template("add.html")

 
@app.route('/search', methods=['GET'])
def search_data():
    return render_template("search_data.html")



    

if __name__=='__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)