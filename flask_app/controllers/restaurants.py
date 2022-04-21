from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.restaurant import Restaurant


@app.route('/favorites')
def favorites():
    return render_template('favorites.html')


# @app.route('/restaurant/generate')
# def generate():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id": session['user_id']
#     }
#     return render_template('generate.html', user=User.get_by_id(data))


@app.route('/restaurant/random')
def random():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    result = Restaurant.generate_random()
    return render_template('result.html', result=result, user=User.get_by_id(data))


@app.route('/restaurant/new')
def new_restaurant():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('new_restaurant.html', user=User.get_by_id(data))


@app.route('/restaurant/create', methods=['POST'])
def create_restaurant():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Restaurant.validate_restaurant(request.form):
        return redirect('/restaurant/new')
    data = {
        "name": request.form['name'],
        "cuisine": request.form['cuisine'],
        "city": request.form['city'],
        "state": request.form['state'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Restaurant.save(data)
    return redirect('/dashboard')


@app.route('/restaurant/<int:id>')
def view_restaurant(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template('view_restaurant.html', restaurant=Restaurant.get_one(data), user=User.get_by_id(user_data), author=Restaurant.get_restaurant_with_user(data))


@app.route('/restaurant/edit/<int:id>')
def edit_restaurant(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template('edit_restaurant.html', restaurant=Restaurant.get_one(data), user=User.get_by_id(user_data))


@app.route('/restaurant/update/<int:id>', methods=['POST'])
def update_restaurant(id):
    if 'user_id' not in session:
        return redirect('/logout')

    if not Restaurant.validate_restaurant(request.form):
        return redirect(f'/restaurant/edit/{id}')

    data = {
        "name": request.form['name'],
        "cuisine": request.form['cuisine'],
        "city": request.form['city'],
        "state": request.form['state'],
        "description": request.form['description'],
        "id": request.form['id']
    }
    Restaurant.update(data)
    return redirect('/dashboard')


@app.route('/restaurant/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Restaurant.destroy(data)
    return redirect('/dashboard')
