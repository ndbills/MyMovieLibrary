# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators


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