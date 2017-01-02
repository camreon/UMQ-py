import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'x\xb0\x82/{\xc3Y\xfa\x92Bz]\x86\x8a\xab\xfaPN\x16M\xd3@'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:umq@postgres:5432/umq'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:umq@postgres:5432/umq'
        # 'postgresql://umq:umq@localhost/umq'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
