import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db    # function we created earlier

# create Blueprint named 'auth'. It needs to know where it's defined,
# so __name__ is passed as an arg
# url_prefix is prepended to all URLs associated with this BP
# TODO: need to import + register this blueprint from the factory __init__.py
bp = Blueprint('auth', __name__, url_prefix='/auth')

# associate URL /register with register view (function)
# this func is called when FLask receives a request to /auth/register
@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        #request.form = speical dict mapping for submitted form keys + values
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        # validate: check if empty
        if not email:
            error = 'Email is required.'
        elif not check_email_syntax(email):
            error = 'Email syntax does not follow xxxx@xxxx.xxx format'
        elif not password:
            error = 'Password is required.'
        # validate: check if email is an email address

        # check if email already exists in db
        # db.execute takes a SQL query with ? placeholders for any user input
            # use a tuple of values to replace the placeholders
            # database lib takes care of escaping the values (to prevent SQL injection)
                # .fecthone() returns one row from the query (fetchall() returns all)
        elif db.execute(
            'select id from user where email = ?', (email,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'insert into user (email, password) VALUES (?, ?)',
                (email, generate_password_hash(password))
            )
            # call this to save the changes to the database
            db.commit()

            # store email address as a session variable for use in the email confirmation page
            session['email'] = email

            # redirect user to the email confirmation page
                # url_for() generates the URL for the login view based on name (endpoint)
                # this is better than writing the URL directly in case of changes
            return redirect(url_for('auth.email_confirmation'))

        # if validation fails, show error to user... flash() stores messages
            # that can be retrieved when rendering the template
        flash(error)

    # renders a template containing the HTML of the register page
        # this should be returned when user navigates to auth/register or receives validation error
    return render_template('auth/register.html')

@bp.route('/email_confirmation', methods=('GET','POST'))
def email_confirmation():
    if request.method == 'GET':
        email = session.get('email', None)
        # email = request.form['email']
        error = None

        if not email:
            error = 'Email read failure'

        if error is None:
            # send email again to the specified address
            print("all is good")
        flash(error)
    return render_template('auth/email_confirmation.html', email=email)

# the endpoint name of a view is 'blueprint_name.view_name' ... so usage would be url_for('auth.login')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        # hashes the submitted password in the same way and checks against db
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session = dict that stores data across requests
            session.clear()

            # b/c login validation succeeds, store user's id in a new session
                # in a cookie that is sent to the browser
                # Flask signs the data to prevent tampering
                # now user's id is available on subsequent requests
            session['user_id'] = user['id']
            return redirect(url_for('mapview'))

        flash(error)

    return render_template('auth/login.html')

# registers a function that runs BEFORE the view function no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    # check if user id is stored in the session... if yes, retrieve from db
    user_id = session.get('user_id')

    # store user info on g.user (which lasts for length of request)
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear() # clears user id from subsequent requests
    return redirect(url_for('index'))

# decorator function can be used to check for user login for each view it's applied to
# returns new view function that wraps the original view
# if user is already loaded in, return the original view
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def check_email_syntax(email):
    # TODO: check that email param is a string
    return re.match(
        "[^@]+@[^@]+\.[^@]+"
        , email)
