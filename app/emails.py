from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from decorators import async

#generalized function to allow asynchronous functions - i.e. so we are not interrupting page loading during email sending
@async
def send_async_email(msg):
	mail.send(msg)

#generalized function for sending emails
def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender = sender, recipients = recipients)
	msg.body = text_body
	msg.html = html_body
	send_async_email(msg)

#email notifying Recommender that an applicant has named them
#will need to autogenerate a password, username is email provided by applicant
#pass in object for current user (applicant) and object for recommender
def recommendation_request(recommender, applicant):
	send_email("[Code for Progress] %s has asked you for a recommendation." % applicant.firstname, ADMINS[0],
	recommender.email,
	render_template("recommendation_email.txt",
	applicant = applicant, recommender = recommender),
	render_template("recommendation_email.html",
	applicant = applicant, recommender = recommender))
