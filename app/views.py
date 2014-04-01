from flask import render_template,flash, request, redirect, g, url_for, session, jsonify
from flask_oauthlib.client import OAuth
from app import app

SECRET_KEY = 'development key'
DEBUG = True
TWITTER_APP_ID = 'eIHUTAYNCwVSwqiIzSduSWXkr'
TWITTER_APP_SECRET = '2K2kQkn8UnKaXft7isaihodDCdXYdrn9lCLWtLKbMIbOMdXdUJ'
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
        tweets=[{'content': {'html':'Welcome'} ,'id':0}]
        posts=twitter.get('statuses/home_timeline.json')
        if posts.data:
            for tweet in posts.data:
                tweets.append({'content': embed_tweet(tweet['id']),'id': tweet['id']})
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

@app.route('/retweet', methods=['POST'])
def retweet():
    resp=twitter.post('statuses/retweet/'+str(request.json['id'])+'.json')
    return jsonify({'html':'resp'})

@app.route('/favorites', methods=['POST'])
def favorites():
    resp=twitter.post('favorites/create.json', data={'id': str(request.json['id'])} )
    return jsonify({'html':'resp'}) 

def embed_tweet(id):
        resp = twitter.get('statuses/oembed.json?id='+str(id)+'&omit_script=true&align=center&maxwidth=550')
        return resp.data





