from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user_model import User


@app.route('/')
def homepage():
    
    user_id=session[user_id]
    user=User.get_one_by_id(user_id)
    
    subscribed_subreddits = user.get_subscribed_subreddits()
    
    posts = []
    for subreddit in subscribed_subreddits:
        subreddit_posts = subreddit.get_all_posts()
    return render_template('index.html')