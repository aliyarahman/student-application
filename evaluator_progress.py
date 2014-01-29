from app import db, models

evaluators = models.User.query.filter_by(role = 4).all()

for evaluator in evaluators:
	completed_evals =0
	evaluations = models.Evaluation.query.filter_by(evaluator_id = evaluator.user_id).all()
	for e in evaluations:
		if e.critical and e.mission and e.community and e.inspire and e.yesno and e.interview:
			completed_evals +=1
	print evaluator.firstname+" "+evaluator.lastname+" has completed\t\t"+str(completed_evals)+"/"+str(len(evaluations))+" evaluations."
