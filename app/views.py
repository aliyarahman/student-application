from flask import render_template, redirect, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from app import app, login_manager, db
from models import User, Recommender, Recommendation
from forms import LoginForm, ProfileForm, RecLoginForm, ShortanswerForm, RecommendationsForm, TechskillsForm, ChecklistForm, RecommenderForm


@login_manager.user_loader
def load_user(userid):
	return Recommender.query.get(userid)

@app.route('/', methods= ['GET'])
@app.route('/index', methods= ['GET'])
@login_required
def index():
	return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = form.get_user()
		login_user(user)
		return render_template('index.html', user = user)
	return render_template('login.html',
		form=form)

@app.route('/checklist', methods = ['GET', 'POST'])
def checklist():
	form = ChecklistForm()
	if form.validate_on_submit():
		return redirect('/profile')
	return render_template('checklist.html',
		form=form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
	if current_user.is_authenticated():
		user = current_user
	else:
		user = None

	form = ProfileForm(obj=user)

	if not form.password or form.password == '':
		del form.password

	if form.validate_on_submit():
		if user:
			flash('Successfully updated your profile.')
		else:
			user = User()

			flash('Congratulations, you just created an account!')

		form.populate_obj(user)
		db.session.add(user)
		db.session.commit()

		if not current_user.is_authenticated():
			login_user(user)

		return redirect('/')

	return render_template('demographic.html', form=form)

@app.route('/shortanswers', methods = ['GET', 'POST'])
@login_required
def shortanswers():
	form = ShortanswerForm(obj=current_user)

	if form.validate_on_submit():
		form.populate_obj(current_user)

		db.session.add(current_user)
		db.session.commit()

		flash("Thanks, we've saved your responses to the short answer section.")
		return redirect('/')
	return render_template('shortanswers.html',
		form=form)

@app.route('/techskills', methods = ['GET', 'POST'])
@login_required
def techskills():
	form = TechskillsForm(obj=current_user)

	if form.validate_on_submit():
		form.populate_obj(current_user)

		db.session.add(current_user)
		db.session.commit()

		flash("Thanks, we've saved your responses to the tech survey.")

		return redirect('/')

	return render_template('techskills.html',
		form=form)

@app.route('/recommendations', methods = ['GET', 'POST'])
@login_required
def recommendations():
	form = RecommendationsForm(obj=current_user)
	
	if form.validate_on_submit():
		form.populate_obj(current_user)

		db.session.add(current_user)
		db.session.commit()

		flash('Your recommendation info has been saved.')
		return redirect('/')

	return render_template('recommendations.html',
		form=form)

@app.route('/finalsubmission')
def finalsubmission():
	return render_template("finalsubmission.html")

@app.route('/help')
def help():
	return render_template("help.html")

@app.route('/received')
def received():
	make_new_recommenders()
	make_blank_recommendations()
#email triggers to info@codeforprogress.org and to recommenders go here, if we want to develop these
	return render_template("received.html")

def make_new_recommenders():
	recommender1 = Recommender.query.filter_by(email = current_user.rec1email).first()
	recommender2 = Recommender.query.filter_by(email = current_user.rec2email).first()
	recommender3 = Recommender.query.filter_by(email = current_user.rec3email).first()
	if not recommender1:
		recommender1 = Recommender(firstname = current_user.rec1firstname, lastname = current_user.rec1lastname, email = current_user.rec1email, phone = current_user.rec1phone, password = generate_recommender_password())
		db.session.add(recommender1)
	if not recommender2:
		recommender2 = Recommender(firstname = current_user.rec2firstname, lastname = current_user.rec1lastname, email = current_user.rec2email, phone = current_user.rec2phone, password = generate_recommender_password())
		db.session.add(recommender2)
	if not recommender3:
		recommender3 = Recommender(firstname = current_user.rec3firstname, lastname = current_user.rec1lastname, email = current_user.rec3email, phone = current_user.rec3phone, password = generate_recommender_password())
		db.session.add(recommender3)
	db.session.commit()

def make_blank_recommendations():
	firstrec = Recommendation(student_id = current_user.user_id, recommender_id = Recommender.query.filter_by(email = current_user.rec1email).first().id)
	secondrec = Recommendation(student_id = current_user.user_id, recommender_id = Recommender.query.filter_by(email = current_user.rec2email).first().id)
	thirdrec = Recommendation(student_id = current_user.user_id, recommender_id = Recommender.query.filter_by(email = current_user.rec3email).first().id)
	db.session.add(firstrec)
	db.session.add(secondrec)
	db.session.add(thirdrec)
	db.session.commit()

def generate_recommender_password():
	import random
	pieces = [random.choice([current_user.firstname,current_user.lastname]),str(random.randint(1000,9999))]
	i = random.choice(pieces)
	password = i
	pieces.remove(i)
	password = i+pieces[0]
	return password

@app.route('/forgot')
def forgot():
	return render_template("forgot.html")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect("http://www.codeforprogress.org")

@app.route('/rec_login', methods = ['GET', 'POST'])
def rec_login():
	form = RecLoginForm()
	if form.validate_on_submit():
		recommender = form.get_recommender()
		login_user(recommender)
		return redirect('/rec_index')
	return render_template('rec_login.html',
		form=form)


@app.route('/rec_index', methods= ['GET'])
@login_required
def rec_index():
	students=current_user.get_students()
	return render_template("rec_index.html", students = students) #pass the students' names to the recommener's menu




@app.route('/rec_form/<student_id>', methods = ['GET', 'POST'])
@login_required
def rec_form(student_id):#pass in the student this is for
	student = User.query.get(student_id) #look up the recommendation that is for this student and this recommender
	recommendation = Recommendation.query.filter_by(student_id=student.user_id, recommender_id=current_user.id).first() #get the recommendation that matches this student and this recommender
	form = RecommenderForm(obj=recommendation) #pull up the form for this recommendation
	if form.validate_on_submit():
		form.populate_obj(recommendation)
		db.session.add(recommendation)
		db.session.commit()
		return redirect('/rec_index')
	return render_template('rec_form.html', form=form, student=student, recommendation=recommendation)#Tell it to pull up a form for this particular recommendation and its corresponding student

@app.route('/rec_finalsubmission')
@login_required
def rec_finalsubmission():
	check = current_user.are_recs_complete()
	return render_template("rec_finalsubmission.html", check = check)

@app.route('/rec_help')
def rec_help():
	return render_template("rec_help.html")

@app.route('/rec_forgot')
def rec_forgot():
	return render_template("rec_forgot.html")

@app.route('/rec_logout')
@login_required
def rec_logout():
	logout_user()
	return redirect("http://www.codeforprogress.org")

@app.route('/rec_received')
@login_required
def rec_received():
	return render_template("rec_received.html")
