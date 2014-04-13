# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine

app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.config['MONGODB_SETTINGS'] = {'DB': 'my_movie_library'}
# app.config["MONGODB_SETTINGS"] = {'DB': "my_movie_library",
								   # 'host': '192.168.1.89'}
app.debug = True
toolbar = DebugToolbarExtension(app)
db = MongoEngine(app)
app.debug = True
# toolbar = DebugToolbarExtension(app)
from project.controllers import *
