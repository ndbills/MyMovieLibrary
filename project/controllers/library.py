# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request, session
from flask.ext.wtf import Form, TextField, validators
from project.model.Library import Library
from project.model.User import User
import json


@app.route('/libraries')
@security('user')
def libraries(user = None):
	libraries = Library.objects(user=user,unit='Movie')
	return render_template('library/master.html', libraries=libraries,user=user)

@app.route('/libraries/<name>')
@security('user')
def library(name,user=None):
	from project.model.Movie import Movie
	library = Library.objects(user=user,name=name,unit='Movie').first()
	return render_template('library/library.html',library=library)

@app.route('/libraries/<name>/<int:index>')
@security('user')
def libraryItem(name, index,user=None):
	return render_template('library/libraryItem.html')
