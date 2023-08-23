from flask_app import connectToMySQL
from flask_app.models.post_model import Post



class Subreddit:
    
    DB="reddit_database"
    
    def __init__(self, id, subreddit_name, description):
        self.id = id
        self.subreddit_name = subreddit_name
        self.description = description
        
    @classmethod
    def get_subreddit_id_by_name(cls, subreddit_name):
        query="SELECT id FROM subreddits WHERE name=%(subreddit_name)s;"
        data={'name':subreddit_name}
        result=connectToMySQL(cls.DB).query_db(query, data)
        return result[0][''] if result else None
    
    
    @classmethod
    def get_posts(self):
        query = """
            SELECT p.*
            FROM posts p
            WHERE p.subreddits_id = %(subreddit_id)s;
        """
        data = {'subreddit_id': self.id}
        results = connectToMySQL(Subreddit.DB).query_db(query, data)
        posts = [Post(result) for result in results]
        return posts
    
    @classmethod
    def get_subscribed_subreddits(cls, user_id):
        from flask_app.models.user_model import User

        query = """
            SELECT s.*
            FROM subreddits s
            WHERE s.users_id = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(User.DB).query_db(query, data)
        
        # Initialize Subreddit instances with the correct arguments
        subscribed_subreddits = [cls(result['id'], result['subreddit_name'], result['description']) for result in results]
        
        return subscribed_subreddits
    
    @classmethod
    def create_new_subreddit(cls, subreddit_name, description, user_id):
        # Import the User class here to avoid circular import
        from flask_app.models.user_model import User

        query = """
            INSERT INTO subreddits (subreddit_name, description, users_id)
            VALUES (%(subreddit_name)s, %(description)s, %(user_id)s)
        """
        data = {
            'subreddit_name': subreddit_name,
            'description': description,
            'user_id': user_id
        }
        new_subreddit_id = connectToMySQL(cls.DB).query_db(query, data)
        return new_subreddit_id

