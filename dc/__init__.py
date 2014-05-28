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

from dc import chef, models


"""

This script is automatically run when the run-script goes 
through to importing from this folder. Some fundamental 
imports, like Flask itself, SQLAlchemy, Migration manager, 
etc happen here. 

The app is an instance of Flask instantiated and stored as 'dc'
And also gets the config file from the instance folder. 

The SQLAlchemy database is instantiated and the migration manager too. 

Then, we just import the contents of the chef and models file.

"""