from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user_model import User
from flask_app.models.post_model import Post
from flask_app.models.subreddit_model import Subreddit
from flask_app.models.comment_model import Comment

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

@app.route('/new_subreddit', methods=['GET', 'POST'])
def create_subreddit():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.get_one_by_id(user_id)
        
        if request.method == 'POST':
            # Retrieve form data
            subreddit_name = request.form.get('subreddit_name')
            description = request.form.get('description')
            
            # Validate the new subreddit data
            errors = Subreddit.validate_new_subreddit(subreddit_name, description)
            if errors:
                for error in errors:
                    flash(error, 'create_subreddit')
                return redirect('/new_subreddit')
            
            # Create the new subreddit
            new_subreddit_id = Subreddit.create_new_subreddit(subreddit_name, description, user_id)
            
            if new_subreddit_id:
                flash("New subreddit created successfully!", 'create_subreddit_success')
                return redirect('/')
            else:
                flash("Failed to create new subreddit.", 'create_subreddit_fail')
        
        return render_template('/', user=user)
    
    flash("You must be logged in to create a subreddit.", 'create_subreddit')
    return redirect('/login')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    

    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    post = Post.get_post_by_id(post_id)
    comments = Comment.get_comments_by_post_id(post_id)

    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            form_data = {
                'comment': request.form.get('comment'),  
                'user_id': user_id,
            }
            Comment.create_new_comment(form_data, post_id)
            flash("Comment added successfully!", 'add_comment')
        else:
            flash("You must be logged in to leave a comment.", 'add_comment')
        
        return redirect(f'/post/{post_id}')

    return render_template('view_post.html', post=post, comments=comments)


@app.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        Post.delete_post(post_id)
        return redirect('/')  # Redirect to the home page after successful deletion
    else:
        flash("Invalid request method.", "error")
        return redirect('/')


@app.route('/post/update/<int:post_id>')
def update_page(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    post = Post.get_post_by_id(post_id)
    
    # Fetch the subreddit name associated with the post
    subscribed_subreddits = Subreddit.get_subscribed_subreddits(user_id)

    return render_template('update_post.html', post=post, subscribed_subreddits=subscribed_subreddits)


@app.route('/post/update/<int:post_id>', methods=['POST'])
def update_post(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    form_data = {
        'title': request.form.get('title'),
        'body': request.form.get('body'),
        'post_id': post_id
    }

    errors = Post.validate_new_post(form_data['title'], form_data['body'])

    if errors:
        post = Post.get_post_by_id(post_id)
        return render_template('update_post.html', post=post, errors=errors)

    Post.update_post(form_data)
    flash("Post updated successfully!", 'update_post')
    return redirect(f'/post/{post_id}')


