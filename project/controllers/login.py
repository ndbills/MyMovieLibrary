# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request, session, redirect, url_for, jsonify
from flask.ext.wtf import Form, TextField, validators
from project.model.User import User

@app.route('/login-ajax', methods=['POST'])
def login():
		email = request.form['email']
		password = request.form['password']
	
		user = User.validateUser(email, password)
		
		if user is not None:
			session['user'] = user.toJSON()
			return jsonify(response='success',type='redirect',path=url_for(endpoint='libraries',_external=True))
		else:
			error = "That email or password is not valid. Please check your credentials and try again."
			return jsonify(response='error',message=error),401

@app.route('/signup-ajax', methods=['POST'])
def signup():
		email = request.form['email']
		password = request.form['password']
		passwordConfirm = request.form['passwordConfirm']

		if password != passwordConfirm:
			error = "The passwords you entered did not match. Please try again."
			return jsonify(response='error',message=error),400

		if len(User.objects(email=email)) > 0:
			error = "The email provided is already in use with another account."
			return jsonify(response='error',message=error),400

		from project.model.Library import Library
		user = User.createUser(email, password)
		user.addRole('user').save()
		session['user'] = user.toJSON()
		Library(user=user, unit='Movie', name='Master').save()
		Library(user=user, unit='Movie', name='Loaned').save()
		return jsonify(response='success',type='redirect',path=url_for(endpoint='libraries',_external=True))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if 'user' in session:
		session.pop('user')
	return redirect(url_for('start'))	
