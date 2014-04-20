# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators

@app.route('/loaned')
@security('user')
def loaned(user=None):
	return render_template('loan/master.html')