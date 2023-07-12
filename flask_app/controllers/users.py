from flask import Flask, render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app import app

@app.route('/')
def index():
    users = User.get_all()
    print(users)
    return render_template("Read.html", users = users)

################# ROOT PAGE SHOWING ALL USERS #################
@app.route('/users', methods=["POST"])
def read_all():
    # Don't forget to redirect after saving to the database.
    return redirect('/')

################# PAGE TO ADD NEW USER INFO TO THE TABLE #################
@app.route('/create/new', methods=['GET', 'POST'])
def create_new():
    return render_template('Create.html')

################# PAGE TO UPDATE USER INFO #################
@app.route('/update/user/<int:user_id>')
def submit_update(user_id):
    user = User.get_user(user_id)
    return render_template('Update.html',user_id=user_id, user=user)

################# PAGE TO SHOW CURRENT USER INFO #################
@app.route('/show/user/<int:user_id>')
def show_user(user_id):
    user = User.get_user(user_id)
    return render_template('User.html', user=user)

################# POST METHOD TO ADD USER #################
@app.route('/user/new', methods=['POST'])
def add_user():
    data = {
        "first": request.form["first"],
        "last": request.form["last"],
        "email": request.form["email"]
        }
    if not User.validate_user(request.form):
        return redirect('/create/new')
    
    User.save(data)
    return redirect('/')

################# POST METHOD TO UPDATE USER #################
@app.route('/submit/update/user/<int:user_id>', methods=['POST'])
def update(user_id):
    data = {
        "first": request.form["first"],
        "last": request.form["last"],
        "email": request.form["email"],
        "id" : user_id
    }

    User.update(data)
    return redirect(f'/show/user/{user_id}')
    

################# POST METHOD TO DELETE USER #################
@app.route('/delete/user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    User.delete(user_id)
    return redirect('/')


