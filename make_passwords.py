from app import db, models
import random

recommenders = models.User.query.filter_by(role = 2).all()

for r in recommenders:
	if r.firstname:
		if r.lastname:	
			pieces = [random.choice([r.firstname, r.lastname]),str(random.randint(1000,9999))]
			i = random.choice(pieces)
			passwd = i
			pieces.remove(i)
			passwd = str(i)+str(pieces[0])
			passwd = passwd.replace(" ", "")
			r.password = passwd
			print r.firstname+" "+r.lastname+"'s password is "+r.password
			db.session.add(r)
print len(recommenders)

db.session.commit()
