import os
from flask import Flask, flash, request, redirect

from flask import send_from_directory
from werkzeug.utils import secure_filename

import glob
from flask import jsonify
from flask.helpers import make_response


UPLOAD_FOLDER = '/tmp/shared'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'o5sGDoMC6LS2L0XIVBwprbgPADbxb3SJCaGLnzxVbCXr14JiWRGJFvAYq7eJoAA8'

def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = app.config['JSONIFY_MIMETYPE']
 
    return response

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
    files = [file[len(app.config["UPLOAD_FOLDER"]):] for file in glob.glob("%s/*"%app.config["UPLOAD_FOLDER"] )]
    return jsonify(files)

@app.route('/data/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
