import unittest
from base_test import BaseTest

class ForgotPasswordTest(BaseTest):

	def test_forgot_password_page(self):
		response = self.client.get("/forgot")
		self.assert200(response)

	def test_submit_reset_form(self):
		response = self.client.post("/forgot", data=dict(email='person@example.com'))
		self.assertRedirects(response, "/forgotConfirmation")

	def runTest(self):
		self.test_forgot_password_page()

if __name__ == '__main__':
	unittest.main()