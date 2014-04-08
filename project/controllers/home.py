# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators


class CreateForm(Form):
    text = TextField(u'Text:', [validators.Length(min=1, max=200)])


@app.route('/')
def start():
    return render_template('home/home.html')


@app.route('/print', methods=['GET', 'POST'])
def printer():
    form = CreateForm(request.form)
    return render_template('printer/index.html')
    # return render_template('printer/print.html', form=form)

@app.route('/model-test')
def model():
	from project.models.User import User
	user = User()
	user.email = 'test@test.com'
	print user.email
	return render_template('printer/index.html')