from flask import render_template
from flask.ext.mail import Message
from app import mail, db, models
from config import ADMINS
from models import User, Recommendation

def send_email(subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender = sender, recipients = recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)

def new_application_submitted(student, completed_app_count):
	send_email("%s just submitted a finished application." % student.firstname, ADMINS[0], ["michelle@codeforprogress.org", "aliya@codeforprogress.org"], render_template("new_application_submitted.txt", student = student), render_template("new_application_submitted.html", student = student, completed_app_count = completed_app_count))


def notify_recommenders(student):
	recommender1 = User.query.filter_by(role=2, email = student.rec1email).first()
	recommender2 = User.query.filter_by(role=2, email = student.rec2email).first()
	recommender3 = User.query.filter_by(role=2, email = student.rec3email).first()
	send_email("%s has asked for your recommendation" % student.firstname, ADMINS[0], [student.rec1email, "aliya@codeforprogress.org"], render_template("notify_recommenders.txt", student=student, recommender=recommender1), render_template("notify_recommenders.html", student = student, recommender=recommender1))
	send_email("%s has asked for your recommendation" % student.firstname, ADMINS[0], [student.rec2email, "aliya@codeforprogress.org"], render_template("notify_recommenders.txt", student=student, recommender=recommender2), render_template("notify_recommenders.html", student = student, recommender=recommender2))
	send_email("%s has asked for your recommendation" % student.firstname, ADMINS[0], [student.rec3email, "aliya@codeforprogress.org"], render_template("notify_recommenders.txt", student=student, recommender=recommender3), render_template("notify_recommenders.html", student = student, recommender=recommender3))

def notify_applicant(student):
        send_email("We've received your application!", ADMINS[0], [student.email, "aliya@codeforprogress.org"], render_template("notify_applicant.txt", student=student), render_template("notify_applicant.html", student = student))

def notify_old_applicant(student):
        send_email("We've notified your recommenders!", ADMINS[0], [student.email, "aliya@codeforprogress.org"], render_template("notify_old_applicant.txt", student=student), render_template("notify_old_applicant.html", student = student))

#new
def remind_recommender(student, recommender):
	send_email("%s has asked for your recommendation" % student.firstname, ADMINS[0], [recommender.email, "aliya@codeforprogress.org"], render_template("remind_recommenders.txt", student=student, recommender=recommender), render_template("remind_recommenders.html", student = student, recommender=recommender))
#new
