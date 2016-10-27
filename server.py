"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    # return a

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show a list of users"""

    users = User.query.all()
    return render_template("users_list.html", users=users)


@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Show user-specific information"""

    user_info = db.session.query(User).filter_by(user_id=user_id).one()
    zipcode = user_info.zipcode
    age = user_info.age
    ratings = user_info.ratings
    print ratings

    return render_template("users_page.html", 
                            zipcode=zipcode,
                            age=age,
                            ratings=ratings)


@app.route('/create-user')
def create_user():
    """Render a form for user to create sign in"""

    return render_template("create_user.html")

@app.route('/submit-account', methods=["POST"])
def submit_account():
    """Get email and password, sign-in (if exist), or create new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).all()

    if not user:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")

@app.route('/login-form')
def log_in():
    """Logs existing user in"""

    return render_template("log_in_form.html")

@app.route('/form-submission', methods=['POST'])
def submit_form():
    """Submits log-in information"""

    email = request.form.get('email')
    password = request.form.get('password')
    user_info = db.session.query(User).filter_by(email=email).all()
    user = user_info[0]
    print user

    
    if user_info == []:
        flash("No account associated with this email address. Create an account below.")
        return redirect('/create-user')
    if user.password == password:
        session["user_id"] = user.user_id
        flash('You were successfully logged in')
        return redirect("/")
    else:
        flash('Invalid credentials')
        return redirect('/login-form')

@app.route('/log-out')
def log_out():
    """Logs user out"""

    del session["user_id"]
    flash('You were successfully logged out')
    return redirect("/")

@app.route('/movies')
def movies_list():

    movies = Movie.query.order_by('title').all()
    return render_template('movies_list.html', movies=movies)

@app.route('/movies/<movie_id>') #is this right?
def show_movie_info(movie_id):
#     """Shows information about a movie"""

    # you want all the ratings objects for a given movie 
    # ratings = db.session.query(Movie.ratings).filter_by(movie_id=movie_id).all()

    return render_template("movie_info.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    app.jinja_env.auto_reload = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)