"""
Main file for the class_recommender
"""

from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_boto3 import Boto3
from gevent.wsgi import WSGIServer
from werkzeug.utils import secure_filename

from utils import parse_info, allowed_file

import os, sys, subprocess
import json

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
        text = subprocess.check_output(["pdftotext", filename, "-"])
        json_info = parse_info(text) 

        with app.app_context():
            ddb = boto_flask.resources[app.config['BOTO3_SERVICES'][0]]
            users = ddb.Table('users')
            users.put_item(Item=json.loads(json_info))

        return json_info, 200


# facebook authentication

from flask import render_template, send_from_directory, session
from flask_oauth import OAuth
from pprint import pprint

app.secret_key = app.config['FB_APP_SECRET']

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FB_APP_ID'],
    consumer_secret=app.config['FB_APP_SECRET'],
    request_token_params={'scope': 'public_profile, user_friends, email'}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None or 'access_token' not in resp:
        return 'Access denied: reason = %s error = %s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(url_for('get_user_info'))

@app.route("/get_user_info")
def get_user_info():
    if not session.get('logged_in'):
        return 'Error: user not logged in'

    data = facebook.get('/me?fields=id, name, first_name, last_name, age_range, link, gender, locale, timezone, updated_time, verified, friends, email').data
    if 'id' in data and 'name' in data and 'email' in data and 'gender' in data and 'age_range' in data:
        user_id = data['id']
        user_name = data['name']
        user_email = data['email']
        user_gender = data['gender']
        user_age_range = data['age_range']

        user = {
            'id': user_id,
            'name': user_name,
            'email': user_email,
            'gender': user_gender,
            'age_range': user_age_range
        }

        return json.dumps(user), 200
    else:
        return 'Error: retrieving info failed'

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('test'))

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
