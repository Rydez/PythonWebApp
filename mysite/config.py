import os

# Default configurations
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = ''''''
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
