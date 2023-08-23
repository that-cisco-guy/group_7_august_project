from flask_app import connectToMySQL


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
    def get_subreddit_by_name(cls, subreddit_name):
        pass
    
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
        query = """
            SELECT s.*
            FROM subreddits s
            WHERE s.users_id = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(User.DB).query_db(query, data)
        subscribed_subreddits = [cls(result) for result in results]
        return subscribed_subreddits
