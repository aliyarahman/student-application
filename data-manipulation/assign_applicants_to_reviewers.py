#Assign applicants to reviewers - to be run once at the beginning of the process

from app import app, db, models, views
import csv
import random

ifile = open('applicant-pre-sort.csv', "rb")
reader = csv.reader(ifile)

# Sort into three bins for assignment, according to Alan's categories
weak =[]
mid = []
strong = []
for row in reader:
	if row[3] ==1:
		weak.append(row[0])
	elif row[3] ==2:
		mid.append(row[0])
	else:
		strong.append(row[0])

#now create three evaluations per student
	


#Commit all to the database 
#db.session.commit()
