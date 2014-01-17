from app import db, models

recommenders = models.User.query.filter_by(role = 2).all()
applicants = models.User.query.filter_by(role = 1).all()

for r in recommenders:
	if r.email:
		r.email = r.email.replace(" ", "")
		r.email = r.email.replace("\t","")
	db.session.add(r)

for a in applicants:
        if a.email:
                a.email = a.email.replace(" ", "")
		a.email = a.email.replace("\t", "")
	if a.rec1email:
                a.rec1email = a.rec1email.replace(" ", "")
                a.rec1email = a.rec1email.replace("\t", "")
        if a.rec2email:
                a.rec2email = a.rec2email.replace(" ", "")
                a.rec2email = a.rec2email.replace("\t", "")
        if a.rec3email:
                a.rec3email = a.rec3email.replace(" ", "")
                a.rec3email = a.rec3email.replace("\t", "")
	db.session.add(a)

db.session.commit()
