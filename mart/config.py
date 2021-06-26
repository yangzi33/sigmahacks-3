# Though configs are not required in this simple demo,
# any apps except this one will have some sorts of configurations.
# This format of configuration is very extensible.
# The config is used by app.config.from_object(Config) called in __init__.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # Configurations for SQLite
    # Take defined database path or confiure a database named app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    # 
    SQLALCHEMY_TRACK_MODIFICATIONS = False