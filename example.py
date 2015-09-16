#!/usr/bin/env python

from flask import Flask, render_template
from flask.ext.wtf import Form
from wtforms import SubmitField, validators
from sweep_field import RowFormField, SweepForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Shh!'
app.config['WTF_CSRF_ENABLED'] = False

class ExampleForm(Form):
    sweep1 = RowFormField(SweepForm, label='Learning Rate', tooltip='Learning rate is the rate of learning')
    sweep2 = RowFormField(SweepForm, label='Bias', tooltip='Bias of something')
    submit = SubmitField('POST')

@app.route('/', methods=['get', 'post'])
def home():
    form = ExampleForm()

    if form.validate_on_submit():
        print str(form.data)

        print '==============='
        print form.sweep1.range()
        print form.sweep2.range()
        print '==============='
    else:
        print form.errors

    return render_template('example.html', form=form)


from flask import request
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    #shutdown_server()
    app.run(debug=True)
