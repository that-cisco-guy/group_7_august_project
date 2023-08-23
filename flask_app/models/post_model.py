from flask import session, redirect
from flask_app import connectToMySQL
from flask_app.models.user_model import User


class Post:
    DB = 'reddit_database'

    def __init__(self, id, subreddits_id, form_data):
        self.id = id
        self.subreddits_id = subreddits_id
        self.title = form_data['title']
        self.body = form_data['body']
        self.users_id = form_data['user_id']

    @classmethod
    def create_new_post(cls, form_data, subreddits):
        query = """
            SELECT subreddits.id
            FROM subreddits
            WHERE subreddits.subreddit_name = %(subreddit_name)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, {'subreddit_name': subreddits})
        
        if result:
            subreddit_id = result[0]['id'] 
            new_form_data = {
                'users_id': session['user_id'],
                'title': form_data['title'],
                'body': form_data['body'],
                'subreddits_id': subreddit_id
            }

            query = """
                INSERT INTO posts (title, post_body, users_id, subreddits_id)
                VALUES (%(title)s, %(body)s, %(users_id)s, %(subreddits_id)s)
            """
            new_post_id = connectToMySQL(cls.DB).query_db(query, new_form_data)
            return new_post_id
        else:
            return None

        
    @classmethod
    def get_threads_by_subreddit(cls, subreddits_id):
        db = cls.DB
        connection = connectToMySQL(db)
        
        query = "SELECT * FROM posts WHERE subreddits_id = %(subreddits_id)s;"
        data = {'subreddits_id': subreddits_id}
        
        threads = connection.query_db(query, data)
        
        return threads
    
    @classmethod
    def get_post_by_id(cls, post_id):
        query = """
            SELECT p.*, u.username
            FROM posts p
            JOIN users u ON p.users_id = u.id
            WHERE p.id = %(post_id)s;
        """
        data = {'post_id': post_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        if result:
            post_data = result[0]
            post = cls(post_data['id'], post_data['subcategories_id'], {
                'title': post_data['title'],
                'body': post_data['body'],
                'user_id': post_data['users_id']
            })
            post.username = post_data['username']  # Add username as an attribute
            return post
        else:
            return None

    @classmethod
    def update_post(cls, form_data):
        query = """
            UPDATE posts
            SET title = %(title)s, body = %(body)s
            WHERE id = %(post_id)s
        """
        data = {
            'title': form_data['title'],
            'body': form_data['body'],
            'post_id': form_data['post_id']
        }
        return connectToMySQL(cls.DB).query_db(query, data)
    

    @classmethod
    def delete_post(cls, post_id):
        connection = connectToMySQL(cls.DB)
        query = "DELETE FROM posts WHERE id = %(post_id)s;"
        data = {'post_id': post_id}
        connection.query_db(query, data)
        
    @staticmethod
    def validate_new_post(title, body):
        errors = []

        if len(title) < 5:
            errors.append("Title must be at least 5 characters long.")
        if len(body) < 20:
            errors.append("Post body must be at least 20 characters long.")

        return errors
