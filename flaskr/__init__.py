# __init__.py
# Contains the application factory for creating the Flask instance
# Also tells Python that flaskr directory is to be treated as a package

import os
import sqlite3
import click

from flask import (Flask, request, session, g, redirect, url_for, abort,
	render_template, flash)

def create_app(test_config=None):
	# create + configure app
	# __name__ = name of current python module
	# instance_relative_config tells app that config files are relative to instance folder
		# instance folder can hold local data that isn't committed to git (config secrets, db files)
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(__name__) # load config from this file

	# set up default config that app will use
	# SECRET_KEY is used to keep client side data set secure (should be overridden w/ random value before deploying)
	# DATABASE = path where SQLite db will be saved
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		USERNAME='admin',
		PASSWORD='default',
		DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
	)
	# allows you to import multiple configs based on the environment
	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

    # ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# create web page to say hello
	@app.route('/hello')
	def hello():
		return 'Hello, JG!'

	# import and register sqlite db
	from . import db
	db.init_app(app)

	# import and register blueprint view for auth
	from . import auth
	app.register_blueprint(auth.bp)

	# unlike the auth blueprint, blog does not have url_prefix
	# index view will be at /, the create view at /create, etc.
	# from . import blog
	# app.register_blueprint(blog.bp)


	from . import geomap
	app.register_blueprint(geomap.bp)
	# associates the endpoint name 'index' with the / url so that
	# url_for('mapview') and url_for('geomap.mapview') point to the same url
	app.add_url_rule('/', endpoint='mapview')

	return app

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv
