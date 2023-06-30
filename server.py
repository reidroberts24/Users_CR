from flask import Flask, render_template, redirect, request
# import the class from user.py
from user import User

app = Flask(__name__)
@app.route('/')
def index():
    users = User.get_all()
    print(users)
    return render_template("Read.html", users = users)

@app.route('/create/new', methods=['POST'])
def create_new():
    return render_template('Create.html')

@app.route('/users', methods=["POST"])
def read_all():
    # Don't forget to redirect after saving to the database.
    return redirect('/')

@app.route('/user/new', methods=['POST'])
def add_user():
    data = {
        "first": request.form["first"],
        "last": request.form["last"],
        "email": request.form["email"]
        }
    User.save(data)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

