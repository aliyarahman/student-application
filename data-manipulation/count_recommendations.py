from app import db, models

complete_apps = models.User.query.filter_by(application_complete =1).all()
zeros = 0
ones = 0
twos = 0
threes = 0

for c in complete_apps:
	completerecs = 0
	recommenders =[]
	for e in [c.rec1email, c.rec2email, c.rec3email]:
		recommenders.append(models.User.query.filter_by(email = e).first())
	for r in recommenders:
		if r:
			rec = models.Recommendation.query.filter_by(recommender_id = r.user_id, student_id = c.user_id).first()
		if rec:
			if rec.recommendation_complete ==1:
				completerecs+=1
	if completerecs == 0:
		zeros +=1
	elif completerecs ==1:
		ones +=1
	elif completerecs ==2:
		twos+=1
	else:
		threes+=1

print str(zeros)+" applications have zero complete recommendations."
print str(ones)+" applications have one complete recommendation."
print str(twos)+" applications have two complete recommendations."
print str(threes)+" applications have three complete recommendations."
