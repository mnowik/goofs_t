#!/bin/bash

cd ..
virtualenv twibs 
cd twibs
bin/pip install flask
bin/pip install Flask-OAuthlib
