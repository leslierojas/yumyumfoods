from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Restaurant:
    db_name = "solo_project"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.cuisine = db_data['cuisine']
        self.city = db_data['city']
        self.state = db_data['state']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO restaurants (name, cuisine, city, state, description, user_id) VALUES (%(name)s,%(cuisine)s,%(city)s,%(state)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE restaurants SET name=%(name)s, cuisine=%(cuisine)s, city=%(city)s, state=%(state)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM restaurants WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM restaurants WHERE id = (%(id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_restaurants(cls):
        query = "SELECT * FROM restaurants LEFT JOIN users ON users.id = restaurants.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_restaurants = []
        print(results)
        for restaurant in results:
            all_restaurants.append(restaurant)
        return all_restaurants

    # @classmethod
    # def generate_random(cls):
    #     query = "SELECT * FROM restaurants ORDER BY RAND() LIMIT 1"
    #     result = connectToMySQL(cls.db_name).query_db(query)
    #     one_restaurant = []
    #     print(result)
    #     for restaurant in result:
    #         one_restaurant.append(restaurant)
    #     return one_restaurant

    @classmethod
    def generate_random(cls):
        query = "SELECT * FROM restaurants LEFT JOIN users ON users.id = restaurants.user_id ORDER BY RAND() LIMIT 1;"
        results = connectToMySQL(cls.db_name).query_db(query)
        restaurant = cls(results[0])
        return restaurant

    @classmethod
    def get_restaurant_with_user(cls, data):
        query = "SELECT * FROM restaurants LEFT JOIN users ON users.id = restaurants.user_id WHERE restaurants.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        restaurant = cls(results[0])  # instantiate restaurant object
        user_info = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        this_user = user.User(user_info)
        restaurant.creator = this_user
        return restaurant

    @staticmethod
    def validate_restaurant(form):
        is_valid = True
        if form['name'] == "":
            flash("Please enter name of a restaurant.", "restaurant")
            is_valid = False
        if form['cuisine'] == "":
            flash("Enter type of cuisine.", "restaurant")
            is_valid = False
        if form['city'] == "":
            flash("Enter city of restaurant location.", "restaurant")
            is_valid = False
        if form['state'] == "":
            flash("Select state of restaurant location.", "restaurant")
            is_valid = False
        if form['description'] == "":
            flash("Enter description of restaurant.", "restaurant")
            is_valid = False
        return is_valid


# "name": request.form['name'],
# "cuisine": request.form['cuisine'],
# "city": request.form['city'],
# "state": request.form['state'],
# "description": request.form['description'],
# "user_id": session['user_id']
