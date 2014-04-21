# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request, jsonify
from flask.ext.wtf import Form, TextField, validators


@app.route('/movies')
def movies():
	return render_template('movies/master.html')

@app.route('/movies/<movieId>')
def movie_item(movieId):
    return render_template('movies/movie.html')

@app.route('/search-movies', methods=['POST'])
@security('user')
def searchMovie(user=None):
	term = request.form['term'];
	if not term:
		return jsonify(response='error',message='Invalid search term'),404
	from tmdb3 import searchMovie
	movies = searchMovie(term)
	if len(movies) == 0:
		return jsonify(response='error',message='No results given'),404
	print movies
	results = []
	limit = 10
	for index in range(len(movies)):
		movie = movies[index]
		if limit <= 0:
			break
		result = {}
		poster = movie.poster
		if poster:
			sizes = poster.sizes()
			if len(sizes) > 0:
				result['poster'] = poster.geturl(sizes[0])
		result['title']	= movie.title
		result['id'] = movie.id
		results.append(result)
		limit -= 1;

	return jsonify(response='success',movies=results)