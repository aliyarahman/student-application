#from sqlalchemy import Column, Integer, db.String, Text, DateTime
#from database import Base
from app import db
import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    firstname = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    email = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    address = db.Column(db.String(90))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    zipcode = db.Column(db.String(10))
    languages = db.Column(db.Text)
    culturalgroups = db.Column(db.Text)
    Q01 = db.Column(db.Text)
    Q02 = db.Column(db.Text)
    Q03 = db.Column(db.Text)
    Q04 = db.Column(db.Text)
    Q05 = db.Column(db.Text)
    Q06 = db.Column(db.Text)
    Q07 = db.Column(db.Text)
    Q08 = db.Column(db.Text)
    Q09 = db.Column(db.Text)
    Q10 = db.Column(db.Text)
    Q11 = db.Column(db.Text)
    basicq1 = db.Column(db.String(45))
    basicq2 = db.Column(db.String(45))
    basicq3 = db.Column(db.String(45))
    basicq4 = db.Column(db.String(45))
    basicq5 = db.Column(db.String(45))
    basicq6 = db.Column(db.String(45))
    basicq7 = db.Column(db.String(45))
    basicq8 = db.Column(db.String(45))
    systemsq1 = db.Column(db.String(45))
    systemsq2 = db.Column(db.String(45))
    systemsq3 = db.Column(db.String(45))
    systemsq4 = db.Column(db.String(45))
    codingq1 = db.Column(db.String(45))
    codingq2 = db.Column(db.String(45))
    codingq3 = db.Column(db.String(45))
    codingq4 = db.Column(db.String(45))
    codingq5 = db.Column(db.String(45))
    codingq6 = db.Column(db.String(45))
    rec1firstname = db.Column(db.String(45))
    rec1lastname = db.Column(db.String(45))
    rec1email = db.Column(db.String(45))
    rec1phone = db.Column(db.String(45))
    rec1how = db.Column(db.Text)
    rec2firstname = db.Column(db.String(45))
    rec2lastname = db.Column(db.String(45))
    rec2email = db.Column(db.String(45))
    rec2phone = db.Column(db.String(45))
    rec2how = db.Column(db.Text)
    rec3firstname = db.Column(db.String(45))
    rec3lastname = db.Column(db.String(45))
    rec3email = db.Column(db.String(45))
    rec3phone = db.Column(db.String(45))
    rec3how = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def __init__(self, username=None, password=None, email=None, firstname=None, lastname=None, \
        phone=None, address=None, city=None, state=None, zipcode=None, languages=None, culturalgroups=None, \
        Q01=None, Q02=None, Q03=None, Q04=None, Q05=None, Q06=None, Q07=None, Q08=None, Q09=None, Q10=None, Q11=None, \
        basicq1=None, basicq2=None, basicq3=None, basicq4=None, basicq5=None, basicq6=None, basicq7=None, basicq8=None, \
        systemsq1=None, systemsq2=None, systemsq3=None, systemsq4=None, codingq1=None, codingq2=None, codingq3=None, \
        codingq4=None, codingq5=None, codingq6=None, rec1firstname=None, rec1lastname=None, rec1email=None, rec1phone=None, rec1how=None, \
        rec2firstname=None, rec2lastname=None, rec2email=None, rec2phone=None, rec2how=None, \
        rec3firstname=None, rec3lastname=None, rec3email=None, rec3phone=None, rec3how=None, timestamp=datetime.datetime.now()):
        
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.languages = languages
        self.culturalgroups = culturalgroups
        self.Q01 = Q01
        self.Q02 = Q02
        self.Q03 = Q03
        self.Q04 = Q04
        self.Q05 = Q05
        self.Q06 = Q06
        self.Q07 = Q07
        self.Q08 = Q08
        self.Q09 = Q09
        self.Q10 = Q10
        self.Q11 = Q11
        self.basicq1 = basicq1
        self.basicq2 = basicq2
        self.basicq3 = basicq3
        self.basicq4 = basicq4
        self.basicq5 = basicq5
        self.basicq6 = basicq6
        self.basicq7 = basicq7
        self.basicq8 = basicq8
        self.systemsq1 = systemsq1
        self.systemsq2 = systemsq2
        self.systemsq3 = systemsq3
        self.systemsq4 = systemsq4
        self.codingq1 = codingq1
        self.codingq2 = codingq2
        self.codingq3 = codingq3
        self.codingq4 = codingq4
        self.codingq5 = codingq5
        self.codingq6 = codingq6
        self.rec1firstname = rec1firstname
        self.rec1lastname = rec1lastname
        self.rec1phone = rec1phone
        self.rec1email = rec1email
        self.rec1how = rec1how
        self.rec2firstname = rec2firstname
        self.rec2lastname = rec2lastname
        self.rec2phone = rec2phone
        self.rec2email = rec2email
        self.rec2how = rec2how
        self.rec3firstname = rec3firstname
        self.rec3lastname = rec3lastname
        self.rec3phone = rec3phone
        self.rec3email = rec3email
        self.rec3how = rec3how
        
    def __repr__(self):
        return '<User %r>' % (self.username)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def __unicode__(self):
        return self.email
		
class Recommendation(db.Model):
	rec_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	recq1 = db.Column(db.Integer)
	recq1ex = db.Column(db.Text)
	recq2 = db.Column(db.Integer)
	recq2ex = db.Column(db.Text)
	recq3 = db.Column(db.Integer)
	recq3ex = db.Column(db.Text)
	recq4 = db.Column(db.Integer)
	recq4ex = db.Column(db.Text)
	recq5 = db.Column(db.Integer)
	recq5ex = db.Column(db.Text)
	recq6 = db.Column(db.Integer)
	recq6ex = db.Column(db.Text)
	rec7 = db.Column(db.Text)
	rec8 = db.Column(db.Text)
	timestamp = db.Column(db.DateTime)
	
	def __init__(self, user_id=None, recq1=None, recq1ex=None, recq2=None, recq2ex=None, recq3=None, \
		recq3ex=None, recq4=None, recq4ex=None, recq5=None, recq5ex=None, recq6=None, recq6ex=None, rec7=None, rec8=None, \
		timestamp=datetime.datetime.now()):
		self.user_id = user_id
		self.recq1 = recq1
		self.recq1ex = recq1ex
		self.recq2 = recq2
		self.recq2ex = recq2ex
		self.recq3 = recq3
		self.recq3ex = recq3ex
		self.recq4 = recq4
		self.recq4ex = recq4ex
		self.recq5 = recq5
		self.recq5ex = recq5ex
		self.recq6 = recq6
		self.recq6ex = recq6ex
		self.rec7 = rec7
		self.rec8 = rec8
		self.timestamp = timestamp
	
	def __repr__(self):
		return '<Recommendation for %r>' % (self.user_id)