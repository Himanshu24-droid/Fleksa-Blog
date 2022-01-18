import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE')
SECRET_KEY = os.getenv(SECRET_KEY)
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = 'fleksa/static/uploads'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
UPLOAD_EXTENSIONS = ['.jpg','.png','.gif','.jpeg']