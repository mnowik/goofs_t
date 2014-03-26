from flask import render_template
import praw
from app import app

@app.route('/')
@app.route('/index')
def index():
	r = praw.Reddit(user_agent='my_cool_application')
	submissions = r.get_subreddit('opensource').get_hot(limit=5)
	return render_template("index.html",
    	submissions=submissions)