from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

class itunesForm(FlaskForm):
	artist = StringField('Enter an artist name.', validators=[Required()])
	email = StringField('Enter an email.', validators=[Required(), Email()])
	results = IntegerField('Enter the number of results.',validators = [Required()])
	submit = SubmitField('Submit')
    
#create class to represent WTForm that inherits flask form

@app.route('/itunes-form')
def itunes_form():
	simpleForm = itunesForm()
	return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
	form = itunesForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
	    artist = form.artist.data # returns a dictionary
	    email = form.email.data
	    results = form.results.data

	    base_url = "https://itunes.apple.com/search"
	    params_diction = {}
	    params_diction["term"] = artist
	    params_diction["country"] = 'US'
	    params_diction["limit"] = results 
	    resp = requests.get(base_url, params = params_diction)
	    response_py = json.loads(resp.text)['results']
	flash('All fields are required!')
	return render_template('itunes-results.html', result_html = response_py)

    #HINT : create itunes-results.html to represent the results and return it

    #return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
