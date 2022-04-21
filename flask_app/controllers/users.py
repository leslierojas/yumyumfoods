from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.restaurant import Restaurant
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if request.form["email"] == "":
        flash("Please enter an email", "login")
    if request.form["password"] == "":
        flash("Please enter a password.", "login")
        return redirect('/')
    if not user_in_db:
        flash("Invalid Email / Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email / Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        "id": session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(user_data), one_restaurant=Restaurant.get_all_restaurants())
