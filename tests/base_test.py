from flask import Flask
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.testing import TestCase

from app import app, db

class BaseTest(TestCase):
	TESTING = True

	def create_app(self):		
		app.config['CSRF_ENABLED'] = False

		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/apply_test.db'

		app.config['TESTING'] = True

		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()