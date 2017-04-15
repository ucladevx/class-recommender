"""
Main file for the class_recommender
"""

from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_boto3 import Boto3
from gevent.wsgi import WSGIServer
from werkzeug.utils import secure_filename

from utils import parse_info, allowed_file

import os, sys
import json
import textract

app = Flask(__name__)
CORS(app)
boto_flask = Boto3(app)
app.config.from_object('config')

#Health check
@app.route('/', methods=['GET'])
def test():
    return "Working!", 200

@app.route('/extract', methods=['POST'])
def extract_text():

    #check if there is a file
    if 'file' not in request.files:
        return 'No file part', 500

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 500

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        #gets the info
        file.save(filename)
        text = textract.process('./' + filename)
        os.remove(filename)
        json_info = parse_info(text) 

        with app.app_context():
            ddb = boto_flask.resources[app.config['BOTO3_SERVICES'][0]]
            users = ddb.Table('users')
            users.put_item(Item=json.loads(json_info))

        return json_info, 200

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
