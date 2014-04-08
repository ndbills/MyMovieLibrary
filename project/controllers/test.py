# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators
import datetime


class CreateForm(Form):
    text = TextField(u'Text:', [validators.Length(min=1, max=200)])


@app.route('/test', methods=['GET', 'POST'])
def test():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        from project.models.Test import Test
        test = Test()
        test.show_string(form.text.data)
        return render_template('test/index.html')
    return render_template('test/test.html', form=form)


@app.route('/test-user')
def test_user():
	from project.models.User import User
	test_user = User(created_at=datetime.datetime.now(), email='test@user.org', password='password', role='admin').save()
	print "date: %s" % test_user.created_at
	#check if test_user exists
	#if yes, return a success render_template
		#else add the user and return some other template
	return render_template('test/test-user.html')