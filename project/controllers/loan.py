# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators

@app.route('/loaned')
@security('user')
def loaned(user=None):
	return render_template('loan/master.html', user=user)

@app.route('/send-reminder', methods=['POST'])
@security('user')
def reminderEmail(user=None):
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