from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin
from gevent.wsgi import WSGIServer
from werkzeug.utils import secure_filename

import os
import textract

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #max file size is 16MB

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            save_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_filename)
            text = textrack.process(save_filename)
            return text, 200

        except:
            return 'Error saving file', 500
    
        


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
