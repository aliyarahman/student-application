#Add sample data to the database for development purposes

from app import app, db, models, views
import csv
import random

#Check to see if evaluator already has a recommender account
#If so, switch to evaluator role and reassign password
#If not, add their account with role =4
ifile = open('selection-committee-accounts.csv', "rb")
reader = csv.reader(ifile)
for row in reader:		
	pieces = [random.choice([row[0],row[1]]),str(random.randint(1000,9999))]
	i = random.choice(pieces)
	password = i
	pieces.remove(i)
	password = i+pieces[0]
		
	s = models.User.query.filter_by(email = row[2]).first()
	
	if s:
		s.role = 4		
		s.password = password
		db.session.add(s)
	else:
		s = models.User(firstname = row[1], lastname = row[0], role = 4, email = row[2], password = password) 
		db.session.add(s)

#Commit all to the database 
db.session.commit()
