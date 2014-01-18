from app import db, models


finishedapplicants = models.User.query.filter_by(application_complete = 1).all()

for f in finishedapplicants:
	if f.rec1email:
		rec1 = models.User.query.filter_by(email = f.rec1email).first()
		if not rec1:
                        print "Missing first recommender ("+f.rec1firstname+" "+f.rec1lastname+", "+f.rec1email+", " +str(f.rec1phone)+") for "+f.firstname+" "+f.lastname+"("+str(f.user_id)+")"

		else:
			thisrec = models.Recommendation.query.filter_by(student_id = f.user_id, recommender_id = rec1.user_id).first()
			if not thisrec:
				print "Missing a blank recommendation for "+rec1.firstname+" "+rec1.lastname+" (re:"+f.firstname+" "+f.lastname+"). Recommender_id is "+str(rec1.user_id)+" and student_id is "+str(f.user_id)+"."

	if f.rec2email:
		rec2 = models.User.query.filter_by(email = f.rec2email).first()
		if not rec2:
			print "Missing second recommender ("+f.rec2firstname+" "+f.rec2lastname+", "+f.rec2email+", " +str(f.rec2phone)+") for "+f.firstname+" "+f.lastname+"("+str(f.user_id)+")"
		else:
			thisrec	= models.Recommendation.query.filter_by(student_id = f.user_id, recommender_id = rec2.user_id).first()
			if not thisrec:
				print "Missing a blank recommendation for "+rec2.firstname+" "+rec2.lastname+" (re:"+f.firstname+" "+f.lastname+"). Recommender_id is "+str(rec2.user_id)+" and student_id is "+str(f.user_id)+"."

	if f.rec3email:
		rec3 = models.User.query.filter_by(email = f.rec3email).first()
		if not rec3:
			print "Missing third recommender ("+f.rec3firstname+" "+f.rec3lastname+") for "+f.firstname+" "+f.lastname
		else:
			thisrec= models.Recommendation.query.filter_by(student_id = f.user_id, recommender_id = rec3.user_id).first()
			if not thisrec:
				print "Missing a blank recommendation for "+rec3.firstname+" "+rec3.lastname+" (re:"+f.firstname+" "+f.lastname+"). Recommender_id is "+str(rec3.user_id)+" and student_id is "+str(f.user_id)+"."



