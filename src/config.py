import os

S3_LOCATION = 'http://your-amazon-site.amazonaws.com/'
S3_KEY = 'YOURAMAZONKEY'
S3_SECRET = 'YOURAMAZONSECRET'
S3_UPLOAD_DIRECTORY = 'what_directory_on_s3'
S3_BUCKET = 'transcriptsdevx'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #max file size is 16MB

SECRET_KEY = "FLASK_SECRET_KEY"
DEBUG = True
PORT = 5000
