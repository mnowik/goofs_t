from flask import render_template,flash, request, redirect, g, url_for, session, jsonify
from flask_oauthlib.client import OAuth
from app import app

SECRET_KEY = 'development key'
DEBUG = True
TWITTER_APP_ID = 'EdP2bzvybB6OoLwvF0g'
TWITTER_APP_SECRET = 'xhFsWVj8NzZB0QrisQo1HBlnkpt2D5OuQfpPkxwvMo0'
oauth =OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key= TWITTER_APP_ID,
    consumer_secret=TWITTER_APP_SECRET
)
   #------------------ OAuth ---------------
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.before_request
def before_request():
    g.user = None
    if 'twitter_user' in session:
        g.user = session['twitter_user']

@app.route('/')
def index():
    if 'twitter_user' in session:
        tweets=[{'html':'Welcome'}]
        posts=twitter.get('statuses/home_timeline.json')
        if posts.data:
            for tweet in posts.data:
                tweets.append(embed_tweet(tweet['id']))
            return render_template("index.html",tweets=tweets)

        
    return render_template('index.html')

@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route('/logout')
def logout():
    session.pop('twitter_user', None)
    return redirect(url_for('index'))


#------------------ functions -------------------

@app.route('/get_tweets')
def get_tweets():
	tweets=[]
	resp = twitter.get('statuses/home_timeline.json')
	if resp.status == 200:
		tweets = resp.data  
	return render_template('view_t.html',tweets=tweets)

def embed_tweet(id):
        resp = twitter.get('statuses/oembed.json?id='+str(id)+'&omit_script=true&align=center&maxwidth=550')
        return resp.data





