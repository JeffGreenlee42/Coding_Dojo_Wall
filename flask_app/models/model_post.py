from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

db = "dojo_wall"

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_post(post):
        isValid = True
        if len(post) < 1:
            isValid = False
            flash("Post content must not be blank.", "post")
            print("isValid is False")
        return isValid
    
    @classmethod
    def get_all(cls):
        query = """SELECT * from posts
                   JOIN users ON posts.users_id = users.id"""
        results = connectToMySQL(db).query_db(query)
        return results
    
    @classmethod
    def create_post(cls, data):
        query = """INSERT INTO posts (content, users_id)
                    VALUES (%(comment)s, %(user_id)s)"""
        result = connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete_post(cls, form_data):
        post_id = int(form_data['post_id'])
        query = f"DELETE FROM posts WHERE id = {post_id}"
        result = connectToMySQL(db).query_db(query)
        return result

