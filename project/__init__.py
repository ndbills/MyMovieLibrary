# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.debug = True
toolbar = DebugToolbarExtension(app)

#import sys, os
#moduleDirectory = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, moduleDirectory)

from project.controllers import *
