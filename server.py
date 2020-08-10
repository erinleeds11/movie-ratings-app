"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View Homepage"""

    return render_template('homepage.html')

@app.route('/movies')
def movie_page():

    movies = crud.get_all_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def movie_id_page(movie_id):
    """show details on a particular movie"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie = movie)

@app.route('/users')
def user_page():

    users = crud.get_all_users()

    return render_template('all_users.html', users = users)

@app.route('/users/<user_id>')
def user_id_page(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user = user)

@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
        return redirect('/')
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')
        return redirect('/login')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def handle_login():

    login_email = request.form.get('login_email')
    login_password = request.form.get('login_password')
    user = crud.get_user_by_email(login_email)
    if login_password == user.password:  
        session['current_user'] = user.user_id
        flash(f'Logged in as {login_email}')
        return redirect('/')
    else:
        flash('Wrong password')
        return redirect('/login')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
