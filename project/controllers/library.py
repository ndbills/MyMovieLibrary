# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request, session, redirect, url_for
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
	if not library:
		return render_template('404.html',message='Unable to find given Library',user=user),404
	return render_template('library/library.html',library=library,user=user)

@app.route('/libraries/<name>/<int:index>')
@security('user')
def libraryItem(name, index,user=None):
	from project.model.Movie import Movie
	library = Library.objects(user=user,name=name,unit='Movie').first()
	if not library:
		return render_template('404.html',message='Unable to find given Library',user=user),404
	movie = library.hydrateUnit(index)
	if not movie:
		return render_template('404.html',message='Unable to find given Movie',user=user),404
	return render_template('library/libraryItem.html',item=movie,user=user)

@app.route('/libraries/<name>/remove/<int:index>', methods=['POST'])
@security('user')
def removelibraryItem(name, index,user=None):
	from project.model.Movie import Movie
	library = Library.objects(user=user,name=name,unit='Movie').first()
	if not library:
		return render_template('404.html',message='Unable to find given Library',user=user),404
	movie = library.hydrateUnit(index)
	if not movie:
		return render_template('404.html',message='Unable to find given Movie',user=user),404
	library.removeUnit(movie)
	return jsonify(response='success',type='redirect',path=url_for(endpoint='library',name=name,_external=True))