#!/bin/bash

cd ..
virtualenv twitter
cd twitter
bin/pip install flask
bin/pip install Flask-OAuthlib
