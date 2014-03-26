from flask import render_template, request, redirect, url_for, session
import praw
from app import app

CLIENT_ID = 'QOkJLc1GlplZgA'
CLIENT_SECRET = 'S5WFGh7QoKFKFxVtsN8YYzThyb4'
REDIRECT_URI = 'http://127.0.0.1:5000/authorize_callback'

r = praw.Reddit('goof')
r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)


# index controls (1) login (2) post display
@app.route('/')
@app.route('/index')
def index():

	# if user is already authenticated
	if 'reddit_oauth' in session:
		if session['reddit_oauth'] is not None:
		
			# display posts...
			print('getting fronptage')
			posts = r.get_front_page(limit=100)
			return render_template("index.html",posts=posts)

	# otherwise, start authentication process
	link_with_refresh = r.get_authorize_url('UniqueKey', 'read', True)
	return render_template("index.html", login_link=link_with_refresh)


# this is called when reddit responds to our auth request
@app.route('/authorize_callback')
def authorized():

	# get the auth code from the request reddit sent us
	code = request.args.get('code', '')

	# store this code in our session 
	session['reddit_oauth'] = code

	# apply this code to praw
	info = r.get_access_information(code)
	
	# redirect to index
	return redirect(url_for('index'))


# logout routine
@app.route('/logout')
def logout():

	# clear the user's oath token from session
	session['reddit_oauth'] = None

	return redirect(url_for('index'))