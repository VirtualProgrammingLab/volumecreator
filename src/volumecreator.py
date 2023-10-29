import os
from flask import Flask, flash, request, redirect

from flask import send_from_directory
from werkzeug.utils import secure_filename

import glob
from flask import jsonify
from flask.helpers import make_response
import requests
import mimetypes
import re
import hashlib

UPLOAD_FOLDER = '/tmp/shared'

def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = "application/json"
    return response

regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def create_fileinfo(file_path):
    name = file_path[len(app.config["UPLOAD_FOLDER"]):]
    size = os.path.getsize(file_path)
    mimetype = get_mimetype(file_path)
    return {"name": name, "size": size, "mimetype" : mimetype}

def add_mimetypes():
    mimetypes.init()
    mimetypes.add_type("application/vnd.kitware", ".vtu")
    mimetypes.add_type("application/vnd.kitware", ".vtp")
    mimetypes.add_type("application/x-vgf", ".vgf")
    mimetypes.add_type("application/x-vgf3", ".vgf3")
    mimetypes.add_type("application/x-vgfc", ".vgfc")

def get_mimetype(file_path):
    mime = mimetypes.guess_type(file_path)
    mimetype = ""
    if mime[0] == "text/plain":
        with open(file_path, 'r') as fr:
            lines = fr.readlines()
        is_uri = all([re.match(regex, line.strip()) for line in lines])
        if is_uri:
            mimetype = "text/uri-list"
        else:
            mimetype = "text/plain"
    elif mime[0] is not None:
        mimetype = mime[0]
    else:
        mimetype = "application/octet-stream"
    return mimetype



# init mimetypes and add missing types
add_mimetypes()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# TODO: Check if necessary, only needed for sessions?
app.config['SECRET_KEY'] = 'o5sGDoMC6LS2L0XIVBwprbgPADbxb3SJCaGLnzxVbCXr14JiWRGJFvAYq7eJoAA8'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify_no_content()
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/list')
def list_files():
    files = []
    for file_path in glob.glob("%s/*" % app.config["UPLOAD_FOLDER"]) :
        files.append(create_fileinfo(file_path))
    return jsonify(files)

@app.route('/list/<name>')
def list_file(name):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], name)
    result = create_fileinfo(file_path)
    return jsonify(result)

@app.route('/data/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/upload/<name>', methods=['POST'])
def post_file_to_s3(name):
    response = request.json
    print(response)
    with open(app.config["UPLOAD_FOLDER"] + '/' + name, 'rb') as f:
        r = requests.put(response["target"], data=f)
        return jsonify(r.status_code)
