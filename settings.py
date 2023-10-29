import os
import re
import string

SHORT_SIZE = 6
SHORT_LENGTH = 16
ORIGINAL_LINK_LENGTH = 500
SYMBOLS = string.ascii_letters + string.digits
SHORT_REGEX = re.compile('^[' + re.escape(SYMBOLS) + ']*$')
REDIRECT_VIEW = 'redirect_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')