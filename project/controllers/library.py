# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request, session, redirect, url_for,jsonify
from flask.ext.wtf import Form, TextField, validators
from project.model.Library import Library
from project.model.User import User
import json


@app.route('/libraries')
@security('user')
def libraries(user = None):
	libraries = Library.objects(user=user,unit='Movie')
	return render_template('library/master.html', libraries=libraries,user=user)

@app.route('/libraries/add', methods=['POST'])
@security('user')
def addLibrary(user = None):
	name = request.form['name']
	library = Library.objects(user=user,unit='Movie',name=name).first()
	if library:
		return jsonify(response='error',message='Library with name %s already exists' % library.name),404
	library = Library(user=user,unit='Movie',name=name).save()
	return jsonify(response='success',type='redirect',path=url_for(endpoint='libraries',_external=True))

@app.route('/libraries/remove', methods=['POST'])
@security('user')
def removeLibrary(user = None):
	name = request.form['name']
	library = Library.objects(user=user,unit='Movie',name=name).first()
	if not library:
		return jsonify(response='error',message='Library requested does not exists'),404
	if library.name == 'Master' or library.name == 'Loaned':
		return jsonify(response='error',message='Library %s cannot be deleted' % library.name),404
	library.delete()
	return jsonify(response='success',type='redirect',path=url_for(endpoint='libraries',_external=True))	

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
	movie = library.hydrateUnit(index-1)
	if not movie:
		return render_template('404.html',message='Unable to find given Movie',user=user),404
	return render_template('library/libraryItem.html',item=movie,user=user,library=library,index=index)

@app.route('/libraries/<name>/remove', methods=['POST'])
@security('user')
def removelibraryItem(name,user=None):
	from project.model.Movie import Movie
	library = Library.objects(user=user,name=name,unit='Movie').first()
	if not library:
		return jsonify(response='error',message='Unable to find the given Library'),404
	index = int(request.form['id'])
	if not index:
		return jsonify(response='error',message='Invalid parameters'),404
	movie = library.hydrateUnit(index-1)
	if not movie:
		return jsonify(response='error',message='Unable to find the given Movie in Library %s' % library.name),404
	
	if library.name == 'Master':
		libraries = Library.objects(user=user,unit='Movie')
		for library in libraries:
			library.removeUnit(movie)
	else:		
		library.removeUnit(movie)

	return jsonify(response='success',type='redirect',path=url_for(endpoint='library',name=name,_external=True))

@app.route('/libraries/<name>/add', methods=['POST'])
@security('user')
def addlibraryItem(name,user=None):
	from project.model.Movie import Movie
	
	library = Library.objects(user=user,name=name,unit='Movie').first()
	if not library:
		return jsonify(response='error',message='Unable to find the given Library'),404
	
	movie_id = request.form['id']	
	if not movie_id:
		return jsonify(response='error',message='Invalid Movie given'),404
	
	from project.model.Movie import Movie
	movie = Movie.objects(tmdb_id=movie_id).first()
	if movie:
		if library.name != 'Master':
			master = Library.objects(user=user,name="Master",unit='Movie').first()
			master.addUnit(movie)
		library.addUnit(movie)
		return jsonify(response='success',type='redirect',path=url_for(endpoint='library',name=name,_external=True))

	from tmdb3 import Movie as tmdbMovie
	movie = tmdbMovie(movie_id)
	if not movie:
		return jsonify(response='error',message='Invalid Movie given'),404
	
	from project.model.Movie import Movie
	movie = Movie.convertMovie(movie)	
	library.addUnit(movie)
	if library.name != 'Master':
			master = Library.objects(user=user,name="Master",unit='Movie').first()
			master.addUnit(movie)

	return jsonify(response='success',type='redirect',path=url_for(endpoint='library',name=name,_external=True))