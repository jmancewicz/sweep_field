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

class Job:
    pass

## Used to save data to populate forms like when cloning
def iterate_over_form(job, form, function, prefix = ['form'], indent = ''):
    if not hasattr(form, '__dict__'): return

    for attr_name in vars(form):
        if attr_name == 'csrf_token' or attr_name == 'flags':
            continue
        attr = getattr(form, attr_name)
        if isinstance(attr, object):
            if isinstance(attr, SubmitField): continue
            iterate_over_form(job, attr, function, prefix + [attr_name], indent + '    ')
        if hasattr(attr, 'data'):
            if (isinstance(attr.data, int) or
                isinstance(attr.data, float) or
                isinstance(attr.data, basestring)):
                key = '%s.%s.data' % ('.'.join(prefix), attr_name)
                function(job, attr, key, attr.data)

def set_data(job, form, key, value):
    if not hasattr(job, 'form_data'): job.form_data = dict()
    job.form_data[key] = value
    print 'set %s %s' % ( key, value)

def get_data(job, form, key, value):
    if key not in job.form_data:
        print '%s is not not saved in job data' % key
    else:
        form.data = job.form_data[key]
        print 'get %s %s' % ( key, value)

def save_form_data_to_job(job, form):
    iterate_over_form(job, form, set_data)

def fill_form_data_from_job(job, form):
    iterate_over_form(job, form, get_data)

@app.route('/', methods=['get', 'post'])
def home():
    form = ExampleForm()

    if form.validate_on_submit():
        print '==============='
        print str(form.sweep1.label), form.sweep1.range()
        print str(form.sweep2.label), form.sweep2.range()
        print '==============='

        print len(form.sweep1.range()) * len(form.sweep2.range())

        job = Job()
        save_form_data_to_job(job, form)
        fill_form_data_from_job(job, form)

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
