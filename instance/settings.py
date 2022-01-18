#import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///fleksa.sqlite'#os.environ.get('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = 'himanshulanjewar'#os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = 'fleksa/static/uploads'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
UPLOAD_EXTENSIONS = ['.jpg','.png','.gif','.jpeg']