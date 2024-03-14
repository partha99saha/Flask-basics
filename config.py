import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    JWT_SECRET = os.environ.get("JWT_SECRET")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")


def get_config():
    env = os.environ.get("ENV", "development")
    if env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


# ENV = development
# ENV = testing
# DATABASE_URI=sqlite:///db.sqlite
# TEST_DATABASE_URI=sqlite:///test_db.sqlite
# JWT_SECRET=12345@Secret
