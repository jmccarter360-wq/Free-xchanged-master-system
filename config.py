import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI')
    API_KEY = os.environ.get('API_KEY')

class ProductionConfig(Config):
    DATABASE_URI = os.environ.get('PROD_DATABASE_URI')

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
    API_KEY = os.environ.get('DEV_API_KEY')

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
    API_KEY = os.environ.get('TEST_API_KEY')
