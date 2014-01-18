from app import db, models

finished = models.User.query.filter_by(application_complete =1, role =1).all()

for f in finished:
	rec1 = models.User.query.filter_by(email = f.rec1email).first()
	rec1.lastname = f.rec1lastname
	db.session.add(rec1)
        rec2 = models.User.query.filter_by(email = f.rec2email).first()
        rec2.lastname =	f.rec2lastname
        db.session.add(rec2)
        rec3 = models.User.query.filter_by(email = f.rec3email).first()
        rec3.lastname =	f.rec3lastname
        db.session.add(rec3)

db.session.commit()
