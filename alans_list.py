from app import db, models
import csv

finished = models.User.query.filter_by(application_complete = 1).all()
for_alan = csv.writer(open('for_alan.csv', 'wb'), delimiter=',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
for f in finished:
	for_alan.writerow([f.user_id, f.lastname,f.firstname])
