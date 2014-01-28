#Add sample data to the database for selection process development purposes

from app import app, db, models
import csv

#Add evaluators

aliya = models.User(firstname = "Aliya", lastname = "Rahman", email = "aliya@codeforprogress.org", password = "P@ssw0rd123	", role = 4)
michelle = models.User(firstname = "Michelle", lastname = "Fox", email = "michelle@codeforprogress.org", password = "P@ssw0rd123", role = 4)
dirk = models.User(firstname = "Dirk", lastname = "Wiggins", email = "dirk@codeforprogress.org", password = "P@ssw0rd123", role = 4)
adam = models.User(firstname = "Adam", lastname = "Unger", email = "adam@codeforprogress.org", password = "P@ssw0rd123", role = 4)

db.session.add(aliya)
db.session.add(michelle)
db.session.add(dirk)

#Add students

db.session.add(models.User(role = 1, firstname = "Joey", lastname = "Fatone", eval1_id = aliya.user_id, eval2_id = michelle.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Doogie", lastname = "Howser", eval1_id = aliya.user_id, eval2_id = michelle.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Steve", lastname = "Urkel", eval1_id = aliya.user_id, eval2_id = michelle.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Huey", lastname = "P", eval1_id = adam.user_id, eval2_id = michelle.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Optimus", lastname = "Prime", eval1_id = adam.user_id, eval2_id = michelle.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Leo", lastname = "Nardo", eval1_id = adam.user_id, eval2_id = michelle.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Medi", lastname = "Ochre", eval1_id = aliya.user_id, eval2_id = adam.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Angry", lastname = "Pig", eval1_id = aliya.user_id, eval2_id = adam.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Danger", lastname = "Mouse", eval1_id = aliya.user_id, eval2_id = adam.user_id, eval3_id = dirk.user_id))
db.session.add(models.User(role = 1, firstname = "Spinder", lastname = "Ella", eval1_id = aliya.user_id, eval2_id = michelle.user_id, eval3_id = adam.user_id))
db.session.add(models.User(role = 1, firstname = "Malifa", lastname = "Cent", eval1_id = aliya.user_id, eval2_id = michelle.user_id, eval3_id = adam.user_id))
db.session.add(models.User(role = 1, firstname = "Win", lastname = "Dow", eval1_id = aliya.user_id, eval2_id = michelle.user_id, eval3_id = adam.user_id))


#Make evals
aliya = models.User.query.filter_by(firstname = "Aliya").first()
dirk = models.User.query.filter_by(firstname = "Dirk").first()
michelle = models.User.query.filter_by(firstname = "Michelle").first()

students = models.User.query.filter_by(role = 1).all()
for s in students:
	db.session.add(models.Evaluation(student_id = s.user_id, evaluator_id = aliya.user_id))
	db.session.add(models.Evaluation(student_id = s.user_id, evaluator_id = dirk.user_id))
	db.session.add(models.Evaluation(student_id = s.user_id, evaluator_id = michelle.user_id))

#Commit all to the database 
db.session.commit()