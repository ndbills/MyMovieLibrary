# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators

@app.route('/login')
def login():
	return render_template('login/master.html')
