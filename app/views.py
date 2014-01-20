from flask import render_template, redirect, flash, request, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from app import app, login_manager, db, mail
from models import User, Recommendation, Evaluation
from forms import LoginForm, ProfileForm, RecLoginForm, ShortanswerForm, RecommendationsForm, TechskillsForm, \
                  ChecklistForm, RecommenderForm, ChangeRecommenderContact, CreateProfileForm, \
                  ResetPasswordForm, ForgotPasswordForm, EvalLoginForm, EvaluatorForm
from emails import new_application_submitted, notify_applicant, notify_recommenders, remind_recommender, send_password_reset
from itsdangerous import Signer, BadSignature

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        if current_user.role == 2:
            return redirect('/rec_index')
        if current_user.role == 0:
            return redirect('/staffview')
        recs=[]
        if current_user.application_complete ==1:
            recs.append(User.query.filter_by(email = current_user.rec1email).first())
            recs.append(User.query.filter_by(email = current_user.rec2email).first())
            recs.append(User.query.filter_by(email = current_user.rec3email).first())
        return render_template('index.html', recs = recs)
    return render_template('login.html',
        form=form)

@app.route('/', methods= ['GET', 'POST'])
@app.route('/index', methods= ['GET', 'POST'])
@login_required
def index():
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.role ==0:
        return redirect('/staffview')
    recs = []
    if current_user.application_complete ==1:
        recs.append(User.query.filter_by(email = current_user.rec1email).first())
        recs.append(User.query.filter_by(email = current_user.rec2email).first())
        recs.append(User.query.filter_by(email = current_user.rec3email).first())
    return render_template("index.html", recs = recs)

#this is the new functionality for users to view their recommenders
@app.route('/myrecommender/<recommender_id>', methods= ['GET', 'POST'])
@login_required
def myrecommender(recommender_id):
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.role ==0:
        return redirect('/staffview')
    #get the recommender sent from the click on index and put it into the form
    recommender = User.query.filter_by(user_id = recommender_id).first()
    form = ChangeRecommenderContact(obj=recommender)
    if recommender.email == current_user.rec1email:
        whichRec = 1
    if recommender.email == current_user.rec2email:
        whichRec = 2
    if recommender.email == current_user.rec3email:
        whichRec = 3
    if form.validate_on_submit():
        form.populate_obj(recommender)
        #commits new recommender info to the database - and this is working
        db.session.add(recommender)
        db.session.commit()
        
        #reload the recommender and put its email into the appropriate place for the current_user
        newrec = User.query.get(recommender.user_id)
        if whichRec==1:
            current_user.rec1email = newrec.email
        if whichRec==2:
            current_user.rec2email = newrec.email
        if whichRec==3:
            current_user.rec3email = newrec.email
        db.session.add(current_user)            
        db.session.commit()
        #send email to the recommender
        remind_recommender(current_user, recommender)

        return redirect('/index')
    return render_template("myrecommender.html", recommender = recommender, form = form)
#this is the new recommender functionality



@app.route('/checklist', methods = ['GET', 'POST'])
def checklist():
    form = ChecklistForm()
    if form.validate_on_submit():
        return redirect('/createprofile')
    return render_template('checklist.html',
        form=form)

@app.route('/createprofile', methods = ['GET', 'POST'])
def createprofile():
    if current_user.is_authenticated():
        user = current_user
    else:
        user = None
    
    form = CreateProfileForm(obj=user)

    if not form.password or form.password == '':
        del form.password
    
    if form.validate_on_submit():
        if user:
            flash('Successfully updated your profile.')
        else:
            user = User()
            user.role = 1
            flash('Congratulations, you just created an account!')

        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

        if not current_user.is_authenticated():
            login_user(user)

        return redirect('/')

    return render_template('createprofile.html', form=form)

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
            user.role = 1
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
    if current_user.role ==2:
        return redirect('/rec_index')

    if current_user.application_complete ==1:
        return redirect('/index')
    
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
    if current_user.role ==2:
        return redirect('/rec_index')

    if current_user.application_complete ==1:
        return redirect('/index')
    
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
    if current_user.role ==2:
        return redirect('/rec_index')

    if current_user.application_complete ==1:
        return redirect('/index')

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
@login_required
def finalsubmission():
    if current_user.role ==2:
        return redirect('/rec_index')

    if current_user.application_complete ==1:
        return redirect('/index')

    return render_template("finalsubmission.html")

@app.route('/help')
def help():
    return render_template("help.html")

@app.route('/staffview', methods = ['GET', 'POST'])
@login_required
def staffview():
    if current_user.role ==1:
        return redirect('/index')
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.role ==0:
        applicants = User.query.filter_by(role = 1).all()
        finishedapplicants = User.query.filter_by(role = 1, application_complete =1).all()
        total_apps = len(applicants)
        complete_apps = len(finishedapplicants)
        return render_template("who_is_done.html", finishedapplicants = finishedapplicants, total_apps = total_apps, complete_apps = complete_apps)

@app.route('/received')
@login_required
def received():
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.application_complete ==1:
        return redirect('/index')

    current_user.application_complete =1
    db.session.add(current_user)
    db.session.commit()
    make_new_recommenders()
    make_blank_recommendations()
    completed_app_count = len(User.query.filter_by(application_complete =1).all())
    new_application_submitted(current_user, completed_app_count)
    notify_applicant(current_user)
    notify_recommenders(current_user)
    return render_template("received.html")

def make_new_recommenders():
    recommender1 = User.query.filter_by(email = current_user.rec1email, role = 2).first()
    recommender2 = User.query.filter_by(email = current_user.rec2email, role = 2).first()
    recommender3 = User.query.filter_by(email = current_user.rec3email, role = 2).first()
    if not recommender1:
        recommender1 = User(firstname = current_user.rec1firstname, lastname = current_user.rec1lastname, email = current_user.rec1email, phone = current_user.rec1phone, password = generate_recommender_password(current_user.rec1firstname, current_user.rec1lastname), role =2, all_recs_complete =0)
        db.session.add(recommender1)
    if not recommender2:
        recommender2 = User(firstname = current_user.rec2firstname, lastname = current_user.rec2lastname, email = current_user.rec2email, phone = current_user.rec2phone, password = generate_recommender_password(current_user.rec2firstname, current_user.rec2lastname), role = 2, all_recs_complete =0)
        db.session.add(recommender2)
    if not recommender3:
        recommender3 = User(firstname = current_user.rec3firstname, lastname = current_user.rec3lastname, email = current_user.rec3email, phone = current_user.rec3phone, password = generate_recommender_password(current_user.rec3firstname, current_user.rec3lastname), role = 2, all_recs_complete =0)
        db.session.add(recommender3)
    db.session.commit()

def make_blank_recommendations():
    firstrec = Recommendation(student_id = current_user.user_id, recommender_id = User.query.filter_by(email = current_user.rec1email, role =2).first().user_id)
    secondrec = Recommendation(student_id = current_user.user_id, recommender_id = User.query.filter_by(email = current_user.rec2email, role = 2).first().user_id)
    thirdrec = Recommendation(student_id = current_user.user_id, recommender_id = User.query.filter_by(email = current_user.rec3email, role = 2).first().user_id)
    db.session.add(firstrec)
    db.session.add(secondrec)
    db.session.add(thirdrec)
    db.session.commit()

def generate_recommender_password(firstname, lastname):
    import random
    
    pieces = [random.choice([firstname,lastname]),str(random.randint(1000,9999))]
    
    i = random.choice(pieces)
    
    password = i
    pieces.remove(i)
    
    password = i+pieces[0]
    password = password.replace(" ","")
    return password

@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    form = ForgotPasswordForm(request.form)

    if request.method == "POST" and form.validate():
        s = Signer(app.config['SECRET_KEY'])
        token = s.sign(request.form['email'])

        send_password_reset(form.get_user(), token)
        return redirect('/forgot_confirmation')

    return render_template("forgot.html", form=form)

@app.route('/forgot_confirmation', methods = ['GET'])
def forgot_confirmation():
    return render_template("forgot_confirmation.html")

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm(request.form)

    if request.method == "POST" and form.validate():
        token = form.token.data

        s = Signer(app.config['SECRET_KEY'])

        try:
            email = s.unsign(token)
        except BadSignature:
            return render_template("reset_invalid_token.html")

        user = User.query.filter_by(email=email).first()

        if user:
            user.set_password(form.password.data)

            print user.password

            login_user(user)

            return redirect("/")
        else:
            return render_template("reset_invalid_token.html")

    token = request.args.get('token', None)

    if not token:
        return render_template("reset_invalid_token.html")

    return render_template("reset_password.html", form=form, token=token)

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
    if current_user.role ==1:
        return redirect('/index')
    
    students = []
    recs =[]
    
    student1 = (User.query.filter_by(rec1email = current_user.email, application_complete =1).all())
    student2 = (User.query.filter_by(rec2email = current_user.email, application_complete =1).all())
    student3 = (User.query.filter_by(rec3email = current_user.email, application_complete =1).all())
    
    recommendations = []    
    
    if student1:
        for s1 in student1:
            students.append(s1)
    if student2:
        for s2 in student2:
            students.append(s2)
    if student3:
        for s3 in student3:
            students.append(s3)
    
    for s in students:
        recommendation = Recommendation.query.filter_by(student_id = s.user_id, recommender_id = current_user.user_id).first()
    
        if recommendation.is_recommendation_complete():
            recommendation.recommendation_complete =1
        recs.append(recommendation)
    
    db.session.add(current_user)
    db.session.commit()
    
    return render_template('rec_index.html',
        students=students, recs = recs)

@app.route('/rec_form/<student_id>', methods = ['GET', 'POST'])
@login_required
def rec_form(student_id):#pass in the student this is for
    if current_user.role ==1:
        return redirect('/index')

    if current_user.all_recs_complete ==1:
        return redirect('/rec_index')

    student = User.query.get(student_id) #look up the recommendation that is for this student and this recommender
    recommendation = Recommendation.query.filter_by(student_id=student.user_id, recommender_id=current_user.user_id).first() #get the recommendation that matches this student and this recommender
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
    if current_user.role ==1:
        return redirect('/index')
    if current_user.all_recs_complete ==1:
        return redirect('/rec_index')

    current_user.are_recs_complete()

    db.session.add(current_user)
    db.session.commit()

    return render_template("rec_finalsubmission.html")

@app.route('/rec_help')
def rec_help():
    if current_user.role ==1:
        return redirect('/index')

    return render_template("rec_help.html")

@app.route('/rec_forgot')
def rec_forgot():
    if current_user.role ==1:
        return redirect('/index')

    return render_template("rec_forgot.html")

@app.route('/rec_logout')
@login_required
def rec_logout():
    logout_user()
    return redirect("http://www.codeforprogress.org")

@app.route('/rec_received')
@login_required
def rec_received():
    if current_user.role ==1:
        return redirect('/index')
    
    if current_user.all_recs_complete == 0:
        return redirect('/rec_finalsubmission')
    
    if current_user.all_recs_complete == 1:
        return redirect('/rec_index')

    return render_template("rec_received.html")

##### Begin code block for selector process

@app.route('/eval_login', methods = ['GET', 'POST'])
def eval_login():
    form = EvalLoginForm()
    if form.validate_on_submit():
        evaluator = form.get_evaluator()
        login_user(evaluator)
        return redirect('/evaluate_index')
    return render_template('eval_login.html',
        form=form)

@app.route('/evaluate_index', methods = ['GET', 'POST'])
@login_required
def evaluate_index():
    if current_user.role ==1:
        return redirect('/index')
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.role ==4:
        assignedapplicants =[]
        evals = Evaluation.query.filter_by(evaluator_id = current_user.user_id).all()
        for e in evals:
            a = User.query.filter_by(user_id = e.student_id).first()
            assignedapplicants.append(a)
        return render_template("evaluate_index.html", assignedapplicants = assignedapplicants, evals=evals, user = current_user)

@app.route('/evaluate/<student_id>', methods = ['GET', 'POST'])
@login_required
def evaluate(student_id):
    if current_user.role ==1:
        return redirect('/index')
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.role ==4:
        student = User.query.filter_by(role = 1, user_id = student_id).first()
        evaluation = Evaluation.query.filter_by(student_id = student.user_id, evaluator_id = current_user.user_id).first()
        recommender1 = User.query.filter_by(email = student.rec1email).first()
        recommender2 = User.query.filter_by(email = student.rec2email).first()
        recommender3 = User.query.filter_by(email = student.rec3email).first()
        rec1 = Recommendation.query.filter_by(student_id = student.user_id, recommender_id = recommender1.user_id).first()
        rec2 = Recommendation.query.filter_by(student_id = student.user_id, recommender_id = recommender2.user_id).first()
        rec3 = Recommendation.query.filter_by(student_id = student.user_id, recommender_id = recommender3.user_id).first()              
        form = EvaluatorForm(obj = evaluation)
        if form.validate_on_submit():
                form.populate_obj(evaluation)
                db.session.add(evaluation)
                db.session.commit()
                return redirect('/evaluate_index')
        return render_template("evaluate.html", f = student, form = form, evaluation =evaluation, rec1 = rec1, rec2=rec2, rec3=rec3)

@app.route('/eval_finalsubmission')
@login_required
def eval_finalsubmission():
    evals_complete = current_user.are_evals_complete()

    db.session.add(current_user)
    db.session.commit()

    print "Evals complete: ", evals_complete

    if current_user.role ==1:
        return redirect('/index')
    if current_user.role ==2:
        return redirect('/rec_index')
    if evals_complete == True:
        #return redirect('/evaluate_index')
        return render_template("eval_received.html")

    return render_template("eval_finalsubmission.html")

@app.route('/eval_help')
def eval_help():
    return render_template("eval_help.html")

@app.route('/eval_forgot')
def eval_forgot():
    return render_template("eval_forgot.html")

@app.route('/eval_logout')
@login_required
def eval_logout():
    logout_user()
    return redirect("http://www.codeforprogress.org")

@app.route('/eval_received')
@login_required
def eval_received():
    if current_user.role ==1:
        return redirect('/index')
    if current_user.role ==2:
        return redirect('/rec_index')
    if current_user.are_evals_complete() ==False:
        return redirect('/eval_finalsubmission')
    if current_user.are_evals_complete() ==True:
        return redirect('/eval_index')
    return render_template("eval_received.html")

##### End code block for selector process