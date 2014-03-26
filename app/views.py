from flask import render_template, request, redirect, url_for, session
import praw
from app import app

CLIENT_ID = 'QOkJLc1GlplZgA'
CLIENT_SECRET = 'S5WFGh7QoKFKFxVtsN8YYzThyb4'
REDIRECT_URI = 'http://127.0.0.1:5000/authorize_callback'

r = praw.Reddit('goof')
r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

@app.route('/')
@app.route('/index')
def index():

	# if user is already authenticated
	if 'reddit_oauth' in session:
		
		# display posts...
		posts = r.get_front_page()
		return render_template("index.html",posts=posts)

	# otherwise, start authentication process
	link_no_refresh = r.get_authorize_url('UniqueKey', 'read')
	return render_template("index.html", login_link=link_no_refresh)

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

