import unittest
from base_test import BaseTest

from app import app, db
from app.models import User

class AccountCreateTest(BaseTest):
	def test_unique_email(self):
		user = User(email='user@example.com')
		db.session.add(user)
		db.session.commit()

		response = self.client.post(
			"/createprofile",
			data=dict(
				firstname='User',
				lastname='User',
				email='user@example.com',
				password='12345',
				retypepassword='12345',
				phone='2025551234',
				address='123 Main Street',
				city='Washington',
				state='DC',
				zip=20001
			)
		)

		self.assert200(response)
		assert 'The email address you provided is already in use.' in response.data