from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)
db = "users"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @staticmethod
    def email_exists(new_email):
        query = """SELECT email FROM users WHERE new_email = email;"""
        result = connectToMySQL(db).query_db(query, new_email)
        if result == False:
            return False
        return True

    @staticmethod
    def validate_user(new_user):
        isValid = True
        if len(new_user['first_name']) < 2:
            flash("First name must be greater than 2 characters", "register")
            isValid = False
        if len(new_user['last_name']) < 2:
            flash("Last name must be greater than 2 characters", "register")
        if not EMAIL_REGEX.match(new_user['email']):
            isValid = False
            flash("Not a valid Email address", "register")
            isValid = False
        if User.email_exists(new_user['email']):
            flash("Email already exists!", "register")
            isValid = False
        if len(new_user['password']) < 8:
            flash("The password must be at least 8 characters!", "register")
            isValid = False
        if not new_user['password'] == new_user['password_confirmation']:
            flash("Password and confirmed password do not Match!", "register")
            isValid = False
        return isValid

    @classmethod
    def add_user(cls, data):
        # pw_hash = bcrypt.generate_password_hash(data['password'])
        # print(f"in add_user: pw_hash is:: {pw_hash}/n")
        query = """INSERT INTO users (first_name, last_name, email, password) 
                   VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s)"""
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s"
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
