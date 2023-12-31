from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('users').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_user(cls, id):
        query = 'SELECT * FROM users WHERE id=%(id)s'
        results = connectToMySQL('users').query_db(query, {'id': id})
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = '''INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
        VALUES (%(first)s, %(last)s, %(email)s, NOW(), NOW())
        '''
        return connectToMySQL('users').query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE users
            SET first_name = %(first)s, 
                last_name = %(last)s, 
                email = %(email)s, 
                updated_at = NOW()
                WHERE id = %(id)s;
            """
        results = connectToMySQL('users').query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, id):
        query = """
            DELETE FROM users
            WHERE id = %(id)s;
        """
        results = connectToMySQL('users').query_db(query, {"id": id})
        return results
    

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first']) == 0 or len(user['last']) == 0 or len(user['email']) == 0:
            flash("Cannot leave any fields blank.")
            is_valid = False
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False

        return is_valid