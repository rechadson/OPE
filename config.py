import os.path


basedir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'storage.db')
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'RMJS VIDROS TCC'