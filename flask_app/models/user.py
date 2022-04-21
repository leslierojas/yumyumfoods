from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import restaurant
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db_name = "solo_project"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = (%(id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        this_user = cls(results[0])
        return this_user

    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, form)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if len(form['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if form['confirmpass'] != form['password']:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid
