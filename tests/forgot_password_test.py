import unittest
from base_test import BaseTest

from app import app, db
from app.models import User

from itsdangerous import Signer

class ForgotPasswordTest(BaseTest):

	def test_forgot_password_page(self):
		response = self.client.get("/forgot")
		self.assert200(response)
		assert ("name=\"email\"" in response.data)

	def test_submit_forgot_form(self):
		response = self.client.post("/forgot", data=dict(email='person@example.com'))
		self.assertRedirects(response, "/forgot_confirmation")

	def test_submit_forgot_invalid_email(self):
		response = self.client.post("/forgot", data=dict(email='blahblah'))

		assert "Hmm, this doesn&#39;t look like an email address." in response.data

	def test_forgot_confirmation_page(self):
		response = self.client.get("/forgot_confirmation")
		self.assert200(response)

	def test_reset_password_page(self):
		response = self.client.get("/reset_password?token=1234.1234567")
		self.assert200(response)
		assert ("name=\"password\"" in response.data)

	def test_reset_uses_token(self):
		response = self.client.get("/reset_password?token=1234.1234567")
		self.assert200(response)
		assert ("1234567" in response.data)

	def test_submit_reset_form(self):
		s = Signer(app.config['SECRET_KEY'])
		token = s.sign('person@example.com')

		user = User(email='person@example.com')
		db.session.add(user)
		db.session.commit()

		response = self.client.post("/reset_password", data=dict(token=token, password='blahblah', password_confirmation='blahblah'))

		self.assertRedirects(response, "/")

	def test_submit_reset_form_invalid_user(self):
		s = Signer(app.config['SECRET_KEY'])
		token = s.sign('person@example.com')

		response = self.client.post("/reset_password", data=dict(token=token, password='blahblah', password_confirmation='blahblah'))

		self.assertTemplateUsed("reset_invalid_token.html")				

	def runTest(self):
		self.test_forgot_password_page()
		self.test_submit_reset_form()

if __name__ == '__main__':
	unittest.main()