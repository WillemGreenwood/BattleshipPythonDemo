from os import environ

class Config:
    DEBUG = int(environ.get('DEBUG', '0'))
    SECRET_KEY = environ.get('SECRET_KEY', 'foobar')
