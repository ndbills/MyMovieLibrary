# -*- coding: utf-8 -*-
__version__ = '0.1'
from functools import wraps
from flask import Flask, session, redirect, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
import sys

sys.path.append('../pytmdb3/')

app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.config['MONGODB_SETTINGS'] = {'DB': 'my_movie_library'}
# app.config["MONGODB_SETTINGS"] = {'DB': "my_movie_library",
								   # 'host': '192.168.1.89'}
# app.debug = True
# toolbar = DebugToolbarExtension(app)
db = MongoEngine(app)
# app.debug = True
# toolbar = DebugToolbarExtension(app)
def security(role=None):
	def wrapper(func):
		@wraps(func)
		def security_check(*args,**kwargs):
			if role == None:
				return func(*args,**kwargs);
			if isinstance(role, list):
				if len(role) == 0:
					return func(*args,**kwargs);
				elif 'user' not in session:
					return redirect(url_for('login', next=request.url))	
				for r in role:
					if r in session['user'].roles:
						return func(*args,**kwargs); 	
				return redirect(url_for('login', next=request.url))	
						
			if 'user' not in session or role not in session['user'].roles:
				return redirect(url_for('login', next=request.url))	
		return security_check
	return wrapper			
	

from project.controllers import *
