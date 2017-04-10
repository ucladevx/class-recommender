from flask import Flask
from flask_cors import CORS, cross_origin
from gevent.wsgi import WSGIServer

app = Flask(__name__)
CORS(app)

@app.route('/')
def test():
    return "Hello World!"

@app.route('/two')
def test_two():
    return "Working!"

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
