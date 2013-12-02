from flask.ext.wtf import Form
from app import db
from models import User
from wtforms import TextField, PasswordField, IntegerField, TextAreaField, RadioField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, ValidationError

class LoginForm(Form):
	username = TextField('username', validators = [Required(message="We need to know your username.")])
	password = PasswordField('password', validators = [Required(message="We need your password.")])

	def validate_username(self, field):
		user = self.get_user()

		if user is None:
			raise ValidationError('Invalid User')

		if user.password != self.password.data:
			raise ValidationError('Invalid Password')

	def get_user(self):
		return db.session.query(User).filter_by(email=self.username.data).first()

class ProfileForm(Form):
	firstname = TextField('firstname', validators = [Required(message='We need to know your first name!')])
	lastname = TextField('lastname', validators = [Required(message='We need to know your last name!')])
	email = TextField('email', validators = [Required(message="We need your email address!"), Email(message="Hmm, your email address doesn't look like an email address.")])
	password = PasswordField('password')
	retypepassword = PasswordField('retypepassword')
	phone = TextField('phone', validators = [Required(message="We need your phone number!")])
	address = TextField('address', validators = [Required(message="We need your address!")])
	city = TextField('city', validators = [Required(message="We'd like to know what city you live in.")])
	state = TextField('state', validators = [Required(message="We'd like to know what state you live in.")])
	zipcode = IntegerField('zipcode', validators = [Required(message="We need your zipcode!")])
	languages = TextAreaField('languages', validators = [Required(message="Please tell us what language(s) you speak.")])
	culturalgroups = TextAreaField('culturalgroups', validators = [Required(message="Please answer question 11.")])
	working = TextAreaField('working', validators = [Required(message="Please answer the last question.")])

	def validate_password(self, field):
		user = self.get_user()

		if not user and self.password.data == None:
			raise ValidationError("Please enter a password")

		if self.password.data and self.password.data != self.retypepassword.data:
			raise ValidationError("Your passwords don't match - try retyping them.")

		if self.password.data and len(self.password.data) < 8:
			raise ValidationError("Your password is a little short - pick one that's at least 8 characters long.")

	def get_user(self):
		return db.session.query(User).filter_by(email=self.email.data).first()


class RecLoginForm(Form):
	username = TextField('username', validators = [Required(message="We need to know your username.")])
	password = PasswordField('password', validators = [Required(message="We need your password.")])

class ShortanswerForm(Form):
	Q01 = TextAreaField('Q01', validators = [Required(message="1")])
	Q02 = TextAreaField('Q02', validators = [Required(message="2")])
	Q03 = TextAreaField('Q03', validators = [Required(message="3")])
	Q04 = TextAreaField('Q04', validators = [Required(message="4")])
	Q05 = TextAreaField('Q05', validators = [Required(message="5")])
	Q06 = TextAreaField('Q06', validators = [Required(message="6")])
	Q07 = TextAreaField('Q07', validators = [Required(message="7")])
	Q08 = TextAreaField('Q08', validators = [Required(message="8")])
	Q09 = TextAreaField('Q09', validators = [Required(message="9")])	
	Q10 = TextAreaField('Q10', validators = [Required(message="10")])
	Q11 = TextAreaField('Q11', validators = [Required(message="11")])			
	Q12 = TextAreaField('Q12', validators = [Required(message="12")])

class TechskillsForm(Form):
	basicq1 = RadioField('basicq1', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq2 = RadioField('basicq2', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])	
	basicq3 = RadioField('basicq3', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq4 = RadioField('basicq4', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq5 = RadioField('basicq5', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq6 = RadioField('basicq6', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq7 = RadioField('basicq7', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq8 = RadioField('basicq8', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	basicq9 = RadioField('basicq9', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required()])
	systemsq1 = RadioField('systemsq1', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	systemsq2 = RadioField('systemsq2', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	systemsq3 = RadioField('systemsq3', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	codingq1 = RadioField('codingq1', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	codingq2 = RadioField('codingq2', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	codingq3 = RadioField('codingq3', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	codingq4 = RadioField('codingq4', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	codingq5 = RadioField('codingq5', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
	codingq6 = RadioField('codingq6', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])


class RecommendationsForm(Form):
	rec1firstname = TextField('rec1firstname', validators = [Required(message="your first recommender's first name")])
	rec1lastname = TextField('rec1lastname', validators = [Required(message="your first recommender's last name")])
	rec1email = TextField('rec1email', validators = [Required(message="your first recommender's email address"), Email("Hmm, your first recommender's email address doesn't look like an email address.")])
	rec1phone = TextField('rec1phone', validators = [Required(message="your first recommender's phone number")])
	rec1how = TextAreaField('rec1how', validators = [Required(message="how you know your first recommender")])
	rec2firstname = TextField('rec2firstname', validators = [Required(message="your second recommender's first name")])
	rec2lastname = TextField('rec2lastname', validators = [Required(message="your second recommender's last name")])
	rec2email = TextField('rec2email', validators = [Required(message="your second recommender's email address"), Email("Hmm, your second recommender's email address doesn't look like an email address.")])
	rec2phone = TextField('rec2phone', validators = [Required(message="your second recommender's phone number")])
	rec2how = TextAreaField('rec2how', validators = [Required(message="how you know your second recommender")])
	rec3firstname = TextField('rec3firstname', validators = [Required(message="your third recommender's first name")])
	rec3lastname = TextField('rec3lastname', validators = [Required(message="your third recommender's last name")])
	rec3email = TextField('rec3email', validators = [Required(message="your third recommender's phone number")])
	rec3phone = TextField('rec3phone', validators = [Required(message="your third recommender's phone number")])
	rec3how = TextAreaField('rec3how', validators = [Required(message="how you know your third recommender")])


class RecommendApplicantForm(Form):
	recq1 = RadioField('recq1', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required(message="1")])
	recq1ex = TextAreaField('recq1ex', validators = [Required(message="1's example box")])
	recq2 = RadioField('recq2', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required(message="2")])
	recq2ex = TextAreaField('recq2ex', validators = [Required(message="2's example box")])
	recq3 = RadioField('recq3', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required(message="3")])
	recq3ex = TextAreaField('recq3ex', validators = [Required(message="3's example box")])
	recq4 = RadioField('recq4', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required(message="4")])
	recq4ex = TextAreaField('recq4ex', validators = [Required(message="4's example box")])
	recq5 = RadioField('recq5', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required(message="5")])
	recq5ex = TextAreaField('recq5ex', validators = [Required(message="5's example box")])
	recq6 = RadioField('recq6', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[Required(message="6")])				
	recq6ex = TextAreaField('recq6ex', validators = [Required(message="6's example box")])
	rec7 = TextAreaField('rec7', validators = [Required(message="7")])
	rec8 = TextAreaField('rec8', validators = [Required(message="8")])
	
class ChecklistForm(Form):
	check1 =  BooleanField('I understand.', validators=[Required()])
	check2 =  BooleanField('I understand.', validators=[Required()])
	check3 =  BooleanField('I understand.', validators=[Required()])
	check4 =  BooleanField('I understand.', validators=[Required()])
	check5 =  BooleanField('I understand', validators=[Required()])
