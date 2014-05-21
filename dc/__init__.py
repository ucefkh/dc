from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

dc = Flask(__name__, instance_relative_config=True)
dc.config.from_object('config')
dc.config.from_pyfile('config.py')

db = SQLAlchemy(dc)
migrate = Migrate(dc, db)

manager = Manager(dc)
manager.add_command('db', MigrateCommand)

from dc import views, models

