from flask import Flask, Response, request,flash, render_template, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from datetime import datetime
import math
import requests
from flask import Flask, request, render_template, jsonify
import os
import csv


from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup


app = Flask(__name__, static_folder="assets", template_folder="templates")
CORS(app)


url=r"C:\Users\ywang\Desktop\DFLT_summary"

    
def save_to_csv(data, path):
    # Determine if we need to write the header
    write_header = not os.path.exists(path)
    
    # Flatten the data dictionary
    flat_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                flat_data[subkey] = subvalue
        else:
            flat_data[key] = value

    with open(path, 'a', newline='') as csvfile:
        fieldnames = list(flat_data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerow(flat_data)
        
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


 





@app.route('/add', methods=['GET', 'POST'])
def save_to_csv(data, path):
    # Determine if we need to write the header
    write_header = not os.path.exists(path)
    
    # Flatten the data dictionary
    flat_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                flat_data[subkey] = subvalue
        else:
            flat_data[key] = value

    with open(path, 'a', newline='') as csvfile:
        fieldnames = list(flat_data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerow(flat_data)

def add_date():
    if request.method == 'POST':
        data = request.json
        print("Received data:")
        print(data)

        # Directory for storing files
        directory =  r'C:\Users\ywang\Desktop\DFLT_summary\sample inforamtion'

        # 1. Save to CSV
        csv_filename = 'all_data.csv'
        csv_path = os.path.join(directory, csv_filename)
       
        save_to_csv(data, csv_path)

       
        # 2. Save to .txt named by pastetype
        txt_filename = f"{data['pastetype']}.txt"
        txt_path = os.path.join(directory, txt_filename)

        with open(txt_path, 'w') as txtfile:
            txtfile.write(json.dumps(data, indent=4))

        return jsonify(message="Data added successfully!")
    
    return render_template("add.html")




 
@app.route('/search', methods=['GET'])
def search_data():
    return render_template("search_data.html")



    

if __name__=='__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)