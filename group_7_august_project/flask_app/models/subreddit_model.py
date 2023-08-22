from flask_app import connectToMySQL

class Subreddit:
    
    DB="reddit_database"
    
    def __init__(self, id, subreddit_name, description):
        self.id = id
        self.subreddit_name = subreddit_name
        self.description = description
        
    # @classmethod
    # def get_subreddit_id_by_name