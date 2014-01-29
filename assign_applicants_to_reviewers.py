#Assign applicants to reviewers - to be run once at the beginning of the process

from app import app, db, models
import csv
import random

#Load csv data for the applicants, where fields are:
# Col 1: user_id
# Col 2: firstname
# Col 3: lastname
# Col 4: Alan's rating where 1 = weak and 3 = strong
ifile = open('applicant-pre-sort.csv', "rb")
reader = csv.reader(ifile)

# Sort applicants into three bins for assignment, according to Alan's categories
weak =[]
middle = []
strong = []
for row in reader:
	if int(row[3]) ==1:
		weak.append(row[0])
	elif int(row[3]) ==2:
		middle.append(row[0])
	else:
		strong.append(row[0])
# Triple the incidence of each user_id so each can be assigned thrice


weak = weak*3
middle.remove("908") #Remove the calibrataor
middle = middle*3
strong = strong*3

# Load the evaluators, removing Victoria and Phil (our backups)
evaluators = models.User.query.filter_by(role = 4).all()
for e in evaluators:
	if e.user_id ==1129 or e.user_id == 1124:
		evaluators.remove(e)


#Assign the calibrator			
for e in evaluators:
	calibrator = models.Evaluation(evaluator_id = e.user_id, student_id = 908)
	db.session.add(calibrator)


# Distribute applicants across evaluators

for category in [weak, middle, strong]:
	while len(category)>0:
		for e in evaluators:
			if len(category)>0:
				pick = random.choice(category)
		# Shannon (1134) cannot have Krysta Atha (59), Jamela Black (590), Leah Libresco (17), or Jenn Stowe (81)
				while (e.user_id == 1134 and pick in [59, 590, 17, 81]):
					pick = random.choice(category)
		# Rashad (253) cannot have Erick Chavarria (user_id = 34)
				while (e.user_id == 253 and pick == 34):
					pick = random.choice(category)
				evaluation = models.Evaluation(evaluator_id = e.user_id, student_id = pick)
				db.session.add(evaluation)
				category.remove(pick)


#Commit all evaluations to the database 
db.session.commit()

