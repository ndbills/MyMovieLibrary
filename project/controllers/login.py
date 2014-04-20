# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request, session, redirect, url_for
from flask.ext.wtf import Form, TextField, validators
from project.model.User import User

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login/master.html')
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
	
		user = User.validateUser(email, password)
		print 'here'
		
		if user is not None:
			session['user'] = user.toJSON()
			return redirect(url_for('libraries'))
		else:
			error = "That email or password is not valid. Please check your credentials and try again."
			return render_template('login/master.html', error=error)

	return render_template('login/master.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('login/signup.html')
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		passwordConfirm = request.form['passwordConfirm']

		if password == passwordConfirm:
			#check unique user
			if len(User.objects(email=email)) == 0:
				from project.model.Library import Library
				#if unique, create user
				user = User.createUser(email, password)
				user.addRole('user').save()
				session['user'] = user.toJSON()
				Library(user=user, unit='Movie', name='Master').save()
				Library(user=user, unit='Movie', name='Borrowed').save()
				return redirect(url_for('libraries'))
			else:
				error = "The email provided is already in use with another account."
				return render_template('login/signup.html', error=error, email=email)
		else:
			error = "The passwords you entered did not match. Please try again."
			return render_template('login/signup.html', error=error, email=email)
	return render_template('login/signup.html')