import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

def get_database_uri():
    db_file = os.path.join(basedir, "db.sqlite")
    if os.path.isfile(db_file):
        return f"sqlite:///{os.path.relpath(db_file, basedir)}"
    else:
        return os.environ.get("DATABASE_URI")

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = get_database_uri()
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
# MAILBOX_EMAIL =
# MAILBOX_PASSWORD =
# SMTP_MAILBOX =
