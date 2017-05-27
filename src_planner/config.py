import os

BOTO3_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
BOTO3_SECRET_KEY= os.environ['AWS_SECRET_ACCESS_KEY']
BOTO3_REGION= 'us-west-2'
BOTO3_SERVICES =['dynamodb']

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #max file size is 16MB

DEBUG = True
PORT = 5000
