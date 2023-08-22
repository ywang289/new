from flask import Flask, Response, request,flash, render_template, make_response, redirect,send_from_directory
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
import zipfile
import matplotlib.pyplot as plt
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, CustomJS, ColumnDataSource
from PIL import Image
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
    sample_name = str(values[0]['timer'])+str(values[0]['board_type']) + str(values[0]['ballsize'])+ str(values[0]['pastetype'])+ str(values[0]['pastesize'])+ str(values[0]['reflow_temp'])

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


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')

def generate_plot(radii, percentages, images):
    x = [i for i in range(1, len(radii) + 1)]
    y = radii

    source = ColumnDataSource(data=dict(
        x=x,
        y=y,
        images=images,
        percentages=percentages
    ))

    p = figure(title="hirox result", plot_width=600, plot_height=400, background_fill_color='lightgrey')
    p.circle('x', 'y', size=10, color="green", source=source)

    hover = HoverTool(tooltips="""
        <div>
            <div>
                <img
                    src="@images" height="200" alt="@percentages" width="200"
                    style="float: left; margin: 0px 15px 15px 0px;"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">@percentages</span>
            </div>
        </div>
    """)

    p.add_tools(hover)

    tap_js = CustomJS(args=dict(source=source), code="""
        var images = source.data['images'];
        var index = source.selected.indices[0];
        var dataURL = images[index];
        var link = document.createElement('a');
        link.href = dataURL;
        link.download = 'image.png';
        link.click();
    """)

    p.js_on_event('tap', tap_js)

    return p

@app.route('/try')
def try_search():
    radii = [3, 5, 8]
    percentages = [39.4, 28, 38.8]
    images = [
        image_to_base64('assets/images/image4.png'),
        image_to_base64('assets/images/image5.png'),
        image_to_base64('assets/images/image6.png')
    ]
    p = generate_plot(radii, percentages, images)
    script, div = components(p)
    return render_template("resume.html", script=script, div=div)


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
    # return render_template("resume.html")
    return render_template("search_data.html")

 





@app.route('/upload', methods=['POST'])
def upload():
    if 'zipfile' not in request.files:
        return "No file part", 400

    file = request.files['zipfile']
    if file.filename == '':
        return "No selected file", 400

    test_result_type = request.form.get("testResultType")
    filename = request.form.get("filename")

    # Create directory if it doesn't exist
    directory = r'C:\Users\ywang\Desktop\DFLT_summary\{}'.format(test_result_type)
    mid_path = os.path.join(directory, filename)
    
    if not os.path.exists(mid_path):
        os.makedirs(mid_path)
    
    
    # Save the uploaded zip file to the server
    zip_path = os.path.join(mid_path, file.filename)
    file.save(zip_path)

    # # Unzip the file into the specified directory
    # with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    #     zip_ref.extractall(directory)

    return "File uploaded and extracted successfully"




@app.route('/plot')
def plot():
    # 创建一个简单的图像
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # 保存图像到一个文件
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Simple Plot')
    plt.savefig('assets/plot.png')

    return send_from_directory('assets', 'plot.png')



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