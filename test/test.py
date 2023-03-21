from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_users():
    users = {}
    with open('users.txt') as f:
        for line in f:
            username, password = line.strip().split(':')
            users[username] = password
    return users


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username not in users or users[username] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    return "Hello, world!"


if __name__ == '__main__':
    app.run(port=5000, debug = True)