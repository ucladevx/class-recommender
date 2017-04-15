from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin
from gevent.wsgi import WSGIServer
from werkzeug.utils import secure_filename

from utils import parse

import os, sys
import textract


app = Flask(__name__)
app.config.from_object('config')
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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

    #save the file if possible
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            file.save(filename)
            text = textract.process('./' + filename)
            os.remove(filename)
            return parse.get_info(text), 200

        except:
            e = sys.exc_info()[0]
            return e, 500
    
if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
