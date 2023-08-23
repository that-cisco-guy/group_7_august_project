from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user_model import User
from flask_app.models.post_model import Post
from flask_app.models.subreddit_model import Subreddit

@app.route('/')
def homepage():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.get_one_by_id(user_id)
        subscribed_subreddits = User.get_subscribed_subreddits(user_id)

        posts = []
        for subreddit in subscribed_subreddits:
            subreddit_posts = subreddit.get_posts()
            posts.extend(subreddit_posts)

        return render_template('index.html', user=user, posts=posts)

    return render_template('index.html') 


@app.route('/new', methods=['GET', 'POST'])
def create_post():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.get_one_by_id(user_id)
        
        if request.method == 'POST':
            # Retrieve form data
            title = request.form.get('title')
            body = request.form.get('body')
            subreddit_name = request.form.get('subreddit_name')  # Assuming you have a form field for subreddit selection
            
            # Validate the new post data
            errors = Post.validate_new_post(title, body)
            if errors:
                for error in errors:
                    flash(error, 'create_post')
                return redirect('/create_post')
            
            # Create the new post
            form_data = {
                'title': title,
                'body': body,
                'user_id': user.id
            }
            new_post_id = Post.create_new_post(form_data, subreddit_name)
            
            if new_post_id:
                flash("New post created successfully!", 'create_post_success')
                return redirect('/')
            else:
                flash("Subreddit not found. Post creation failed.", 'create_post_fail')

        subscribed_subreddits = Subreddit.get_subscribed_subreddits(user_id)
        return render_template('create_post.html', user=user, subscribed_subreddits=subscribed_subreddits)
    
    flash("You must be logged in to create a post.", 'create_post')
    return redirect('/login')
