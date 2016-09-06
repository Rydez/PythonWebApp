import os

# Default configurations
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '''\x02/\x8d\x85\r?-v\xa0'\r\xad;\xfa=\x11\xb9\x19}\x14\x81\xec\xe1\xc4'''
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False