from flask import Flask 
from flask import render_template

app = Flask(__name__)
@app.route('/') 
def main():
    return render_template('index.html')


if __name__ == '__main__': from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from recognize import main
from detect_age import age
from detect_gender import gender
from werkzeug.utils import secure_filename
import os
import urllib.request
import json
import ssl
import io
import os
import re
from os.path import join, dirname, realpath
import jinja2
import shutil 

app = Flask(__name__, template_folder='templates', static_url_path='')

UPLOAD_FOLDER = join(dirname(realpath(__file__)), './static')
UPLOAD_FOLDER2 = join(dirname(realpath(__file__)), './images') 
print(UPLOAD_FOLDER,UPLOAD_FOLDER2)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2']=UPLOAD_FOLDER2

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER2'],filename), os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            """
            file_name=os.path.join(os.path.dirname(__file__),filename)
            (file_name)
            with io.open(file_name,'rb') as image_file:
                content=image_file.read()
            """
            name,probability_name= main(filename)
            age_range,probability_age = age(filename)
            gender_range,probability_gender = gender(filename)
            text = name + ", " + str(probability_name)
            age_text = age_range + ", " + str(probability_age)
            gender_text = gender_range + ", " + str(probability_gender)
            return render_template('index.html',imgURL=filename, text = text, age_text = age_text, gender_text = gender_text)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
    app.debug = True
    app.run()