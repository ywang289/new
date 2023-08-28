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
from sqlalchemy import or_, and_

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder="assets", template_folder="templates")
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class BGAs(db.Model):
    id = db.Column(db.String, primary_key=True)
    timer = db.Column(db.String(50))
    board_type = db.Column(db.String(50))
    ball_size = db.Column(db.Integer)
    paste_type = db.Column(db.String(200))
    paste_size = db.Column(db.Integer)
    reflow_temp= db.Column(db.Integer)
    reflow_time = db.Column(db.Integer)
    board_list = db.Column(db.JSON)
    paste_list = db.Column(db.JSON)
    hirox_result= db.Column(db.Text)
    shear_test_result= db.Column(db.Integer)
    drop_test_result = db.Column(db.Integer)
    
    

    def __init__(self,timer, id, board_type, ball_size, paste_type, paste_size, reflow_temp, reflow_time, board_list, paste_list,hirox_result,shear_test_result,drop_test_result):
        self.id= id
        self.timer=timer
        self.board_type= board_type
        self.ball_size= ball_size
        self.paste_type= paste_type
        self.paste_size= paste_size
        self.reflow_temp= reflow_temp
        self.reflow_time= reflow_time
        self.board_list= board_list
        self.paste_list= paste_list
        self.hirox_result= hirox_result
        self.drop_test_result= drop_test_result
        self.shear_test_result= shear_test_result

class NONBGAS(db.Model):
    id = db.Column(db.String, primary_key=True)
    timer = db.Column(db.String(50))
    type = db.Column(db.String(50))
    description= db.Column(db.String(200))
    hirox_result= db.Column(db.Text)
    shear_test_result= db.Column(db.Integer)
    drop_test_result = db.Column(db.Integer)
    
    def __init__(self, id, timer,type,description,hirox_result,shear_test_result,drop_test_result):
        self.id= id
        self.timer=timer
        self.type=type
        self.description= description
        self.hirox_result= hirox_result
        self.drop_test_result= drop_test_result
        self.shear_test_result= shear_test_result

@app.before_first_request
def create_tables():
    db.create_all()




# url=  r'C:\Users\ywang\Desktop\DFLT_summary\sample inforamtion'
url = '/Users/wangyifan/Desktop/DFLT_summary'


    
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

@app.route('/show_data')
def show_data():
    bgas = BGAs.query.all()
    nonbgas =  NONBGAS.query.all()
    return render_template('show_data.html', bgas=bgas, nonbgas= nonbgas)


@app.route('/add', methods=['GET', 'POST'])

def add_date():
    if request.method == 'POST':
        data = request.json['Data']
        print(data)
        if data['choice']=='bga':
        
            new_bga = BGAs(
                    id = data["board_type"] + data["pastetype"] + data["timer"],
                    timer=data["timer"],
                    board_type=data["board_type"],
                    ball_size=data["ballsize"],
                    paste_type=data["pastetype"],
                    paste_size=data["pastesize"],
                    reflow_temp=data["reflow_temp"],
                    reflow_time=data["reflow_time"],
                    board_list=json.dumps(data["board_list"]),
                    paste_list=json.dumps(data["paste_list"]),
                    hirox_result= data["singlePhotoResult"],
                    drop_test_result=data["drop_result"],
                    shear_test_result=data["shear_result"],
        
            )

            # Add to the database session and commit
            db.session.add(new_bga)
            db.session.commit()
        else:
            print("this is before the database")
            print(data)
            
            new_nonbga=NONBGAS(
                id = data["type"]+ data["timer"],
                timer=data["timer"],
                type= data['type'],
                description=data['description'],
                hirox_result= data["singlePhotoResult"],
                drop_test_result=data["drop_result"],
                shear_test_result=data["shear_result"],

            )
            db.session.add(new_nonbga)
            db.session.commit()

        # print("Received data:")
        # print(data)

        # # Directory for storing files
        # directory =  r'C:\Users\ywang\Desktop\DFLT_summary\sample inforamtion'
        # directory= '{}/{}'.format(url,'sample inforamtion')

        # # 1. Save to CSV
        # csv_filename = 'all_data.csv'
        # csv_path = os.path.join(directory, csv_filename)
    
        # save_to_csv(data, csv_path)
          

        return jsonify(message="Data added successfully!")
    

    return render_template("new_add.html")


 
@app.route('/search', methods=['GET'])
def search_data():
    # return render_template("resume.html")
    return render_template("search_bar.html")

 

from werkzeug.utils import secure_filename
from flask import request, jsonify
def save_to_number_csv(filename, numberValue, csv_path):
    # 检查文件是否存在
    file_exists = os.path.exists(csv_path)
    
    with open(csv_path, 'a', newline='') as csvfile:
        fieldnames = ['filename', 'numberValue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 如果文件不存在，则写入标题行
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({'filename': filename, 'numberValue': numberValue})

@app.route('/upload', methods=['POST'])
def upload():
    # 获取 userData 字符串
    user_data_str = request.form.get('userData')
    print(user_data_str)
   
    if not user_data_str:
        return jsonify(status="error", message="Parameter 'userData' is missing"), 400

    # 尝试解析 JSON
    try:
        userData = json.loads(user_data_str)
    except json.JSONDecodeError:
        return jsonify(status="error", message="Invalid format for 'userData'. Expecting valid JSON."), 400

    # TODO: 这里可以处理其他的请求数据，例如文件上传

    # 如果一切正常，返回成功的响应
    return jsonify(status="success", message="File uploaded successfully")










@app.route('/save_image', methods=['POST'])
def save_image():
    # data = request.json
    # base64_image = data['image'].split(',')[1]  
    # filename = data['filename']  # 获取文件名

    # image_data = base64.b64decode(base64_image)

    # directory= '{}/{}'.format(url,'sample inforamtion')
    # path = os.path.join(directory, filename)
    
    # with open(path, 'wb') as f:
    #     f.write(image_data)

    return jsonify(status="success")
    

if __name__=='__main__':

    app.run(host='0.0.0.0', port=8081, debug=True)