import unittest
from base_test import BaseTest

from app.models import User
from app import db

class CreateUserTest(BaseTest):
	def test_create_user(self):
		user = User()
		db.session.add(user)
		db.session.commit()

		assert user in db.session

	def runTest(self):
		self.test_create_user()

if __name__ == '__main__':
	unittest.main()