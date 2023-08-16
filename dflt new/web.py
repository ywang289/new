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
import base64


from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup


app = Flask(__name__, static_folder="assets", template_folder="templates")
CORS(app)


url=r"C:\Users\ywang\Desktop\DFLT_summary"

    
def save_to_csv(data, path):
    # Determine if we need to write the header
    write_header = not os.path.exists(path)
    
    # Flatten the data dictionary
    values = list(data.values())
    print(values)
    sample_name = str(values[0]['board_type']) + str(values[0]['ballsize'])+ str(values[0]['pastetype'])+ str(values[0]['pastesize'])+ str(values[0]['reflow_temp'])

    # [{'board_type': 'w', 'ballsize': 'w', 'pastetype': 'wer', 'pastesize': 'wer', 'reflow_temp': '110', 'reflow_time': '20', 
    #   'board_list': {'Boron': '12', 'Carbon': '13', 'Aluminium': '15', 'Beryllium': '56'}, 
    #   'paste_list': {'Boron': '12', 'Carbon': '13', 'Aluminium': '15', 'Beryllium': '56'}}]

    # Flatten the data dictionary

    flat_data = {"sample_name": sample_name}
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
          

        return jsonify(message="Data added successfully!")
    

    return render_template("add.html")


 
@app.route('/search', methods=['GET'])
def search_data():
    return render_template("search_data.html")

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'files' not in request.files:
            return jsonify(status="error", message="No file part")

        test_result_type = request.form.get("testResultType")
        print(f"Test Result Type: {test_result_type}")
        uploaded_files = request.files.getlist('files')

        # Create a directory based on test_result_type
        # directory = r'C:\Users\ywang\Desktop\DFLT_summary\{}'.format(test_result_type)
        directory = r'C:\Users\ywang\Desktop\DFLT_summary'
        if not os.path.exists(directory):
            os.makedirs(directory)

        for file in uploaded_files:
            if file.filename == '':
                return jsonify(status="error", message="No selected file")

            # Save the uploaded file in the created directory
            file_path = os.path.join(directory, file.filename)
            try:
                file.save(file_path)
                print(f"Saved file: {file.filename}")
            except Exception as e:
                print(f"Error saving file: {str(e)}")


        return jsonify(status="success")
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(status="error", message=str(e))


@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
    base64_image = data['image'].split(',')[1]  
    filename = data['filename']  # 获取文件名

    image_data = base64.b64decode(base64_image)

    directory = r'C:\Users\ywang\Desktop\DFLT_summary\sample inforamtion'
    path = os.path.join(directory, filename)
    
    with open(path, 'wb') as f:
        f.write(image_data)

    return jsonify(status="success")
    

if __name__=='__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)