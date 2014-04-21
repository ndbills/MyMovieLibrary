# -*- coding: utf-8 -*-
__version__ = '0.1'
import sys
sys.path.append('../pytmdb3/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')

from functools import wraps
from flask import Flask, session, redirect, url_for, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine


from tmdb3 import set_key

app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.config['MONGODB_SETTINGS'] = {'DB': 'my_movie_library'}
app.config['SMTP_USER'] = "my.movie.library.reminder@gmail.com"
app.config['SMTP_PASSWORD'] = "1 LikemoVies&p0pCO7n"
app.config['SMTP_SERVER'] = "smtp.gmail.com:587"
app.config['TMDB_API_KEY'] = "542606a6ccff81a0337dc370a0cbfc37"
set_key(app.config['TMDB_API_KEY'])

# app.config["MONGODB_SETTINGS"] = {'DB': "my_movie_library",
								   # 'host': '192.168.1.89'}
app.debug = True
# toolbar = DebugToolbarExtension(app)
db = MongoEngine(app)
# app.debug = True
# toolbar = DebugToolbarExtension(app)
def security(role=None):
	def wrapper(func):
		@wraps(func)
		def security_check(*args,**kwargs):
			import json	
			user = None
			if 'user' in session:
				from project.model.User import User
				user = json.loads(session['user'])
				user = User.objects(email=user['email']).first()
				kwargs['user'] = user
			
			if role == None:
				return func(*args,**kwargs);
			if isinstance(role, list):
				if len(role) == 0:
					return func(*args,**kwargs);
				elif user == None:
					return redirect(url_for('start', next=request.url))	
				
				for r in role:
					if r in user.roles:
						return func(*args,**kwargs); 	
				return redirect(url_for('start', next=request.url))	
			
			if user == None or role not in user.roles:
				return redirect(url_for('start', next=request.url))	
			
			return func(*args,**kwargs); 	
		return security_check
	return wrapper			

from project.controllers import *
