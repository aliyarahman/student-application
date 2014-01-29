from app import db, models

applicants = models.User.query.filter_by(application_complete =1).all()

#print "Name \t\t|\tComplete Evaluations \t|\tYeses\t|\tAverage score"
for a in applicants:
	evals = models.Evaluation.query.filter_by(student_id = a.user_id).all()
	yeses = 0
	complete = 0
	totalscores =[]
	averagescore = 0
	for e in evals:
		if e.evaluation_complete == 1:
			complete +=1
			totalscores.append((int(critical)+int(mission)+int(community)+int(inspire)))
		if e.yesno =='Yes':
			yeses +=1	
			averagescore = (sum(totalscores) / float(len(totalscores)))
	print "{0} {1}:\t  {2}/3 complete evals, {3} yeses, average score of  {4}/24".format(a.firstname, a.lastname,complete, yeses, averagescore)
