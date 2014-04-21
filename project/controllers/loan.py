# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request, jsonify
from flask.ext.wtf import Form, TextField, validators

@app.route('/loaned')
@security('user')
def loaned(user=None):
	return render_template('loan/master.html', user=user)

@app.route('/send-reminder', methods=['POST'])
@security('user')
def reminderEmail(user=None):
	import smtplib
	from_addr = user.email
	to_addr = request.form['email']
	subject = request.form['subject'] or "Movie Return Reminder"
	movie_id = request.form['movie']
	if not movie_id:
		return jsonify(response='error',message='Invalid Movie given'),404
	from project.model.Movie import Movie
	movie = Movie.objects(id=movie_id).first()
	if not movie:
		return jsonify(response='error',message='Invalid Movie given'),404
	loan = movie.getLoan(user)
	if not loan:
		return jsonify(response='error',message='Invalid Movie given'),404
	message = request.form['message'] or "The movie %s, borrowed form %s is due on %s" % (movie.title, user.email, loan.expected_return_date)
	login = app.config['SMTP_USER']
	password = app.config['SMTP_PASSWORD']
	smtpserver= app.config['SMTP_SERVER']

	header  = 'From: %s\n' % from_addr
	header += 'To: %s\n' % to_addr
	header += 'Subject: %s\n\n' % subject
	message = header + message
 
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login,password)
	problems = server.sendmail(from_addr, to_addr, message)
	server.quit() 
	return jsonify(response='success',type="reload")

@app.route('/loan-movie', methods=['POST'])
@security('user')
def createLoan(user=None):
	import smtplib
	from datetime import datetime
	borrower = request.form['email']
	return_date = request.form['date'] or None
	movie_id = request.form['movie']
	if return_date:
		return_date = datetime.strptime(return_date, '%m/%d/%Y')
	
	if not movie_id:
		return jsonify(response='error',message='Invalid Movie given'),404
	from project.model.Movie import Movie
	movie = Movie.objects(id=movie_id).first()
	if not movie:
		return jsonify(response='error',message='Invalid Movie given'),404
	
	from project.model.Loan import Loan
	loan = Loan.objects(user=user,movie=movie).first()
	if loan:
		return jsonify(response='error',message='A loan already exists for this movie'),404	

	loan = Loan.create(user,movie,borrower,return_date)
	from project.model.Library import Library
	borrowed_lib = Library.objects(user=user,unit="Movie",name="Borrowed").first()
	borrowed_lib.addUnit(movie)

	return jsonify(response='success',type="reload")	