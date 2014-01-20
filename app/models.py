
from app import db
import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    firstname = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    address = db.Column(db.String(90))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    zipcode = db.Column(db.String(10))
    languages = db.Column(db.Text)
    culturalgroups = db.Column(db.Text)
    working = db.Column(db.Text)
    school = db.Column(db.Text)
    appsource = db.Column(db.String(50))
    Q01 = db.Column(db.Text)
    Q02 = db.Column(db.Text)
    Q03 = db.Column(db.Text)
    Q04 = db.Column(db.Text)
    Q05 = db.Column(db.Text)
    Q06 = db.Column(db.Text)
    Q07 = db.Column(db.Text)
    Q08 = db.Column(db.Text)
    Q09 = db.Column(db.Text)
    Q10 = db.Column(db.Text)
    Q11 = db.Column(db.Text)
    Q12 = db.Column(db.Text)
    basicq1 = db.Column(db.String(45))
    basicq2 = db.Column(db.String(45))
    basicq3 = db.Column(db.String(45))
    basicq4 = db.Column(db.String(45))
    basicq5 = db.Column(db.String(45))
    basicq6 = db.Column(db.String(45))
    basicq7 = db.Column(db.String(45))
    basicq8 = db.Column(db.String(45))
    basicq9 = db.Column(db.String(45))
    systemsq1 = db.Column(db.String(45))
    systemsq2 = db.Column(db.String(45))
    systemsq3 = db.Column(db.String(45))
    systemsq4 = db.Column(db.String(45))
    codingq1 = db.Column(db.String(45))
    codingq2 = db.Column(db.String(45))
    codingq3 = db.Column(db.String(45))
    codingq4 = db.Column(db.String(45))
    codingq5 = db.Column(db.String(45))
    codingq6 = db.Column(db.String(45))
    rec1firstname = db.Column(db.String(45))
    rec1lastname = db.Column(db.String(45))
    rec1email = db.Column(db.String(45))
    rec1phone = db.Column(db.String(45))
    rec1how = db.Column(db.Text)
    rec2firstname = db.Column(db.String(45))
    rec2lastname = db.Column(db.String(45))
    rec2email = db.Column(db.String(45))
    rec2phone = db.Column(db.String(45))
    rec2how = db.Column(db.Text)
    rec3firstname = db.Column(db.String(45))
    rec3lastname = db.Column(db.String(45))
    rec3email = db.Column(db.String(45))
    rec3phone = db.Column(db.String(45))
    rec3how = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    application_complete = db.Column(db.Integer, default = 0)
    recommendations = db.relationship('Recommendation', backref = 'requester', lazy = 'dynamic')
    role = db.Column(db.Integer)    
    all_recs_complete = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def __unicode__(self):
        return self.email

    def profile_complete(self):
        if self.email and self.password and self.culturalgroups and self.working:
           return True
        return False

    def short_questions_complete(self):
        if self.Q01 and self.Q02 and self.Q03 and self.Q04 and self.Q05 and self.Q06 and \
           self.Q07 and self.Q08 and self.Q09 and self.Q10 and self.Q11 and self.Q12:
           return True
        return False

    def tech_questions_complete(self):
        if self.basicq1 and self.basicq2 and self.basicq3 and self.basicq4 and \
           self.basicq5 and self.basicq6 and self.basicq7 and self.basicq8 and self.basicq9:
           return True
        return False

    def recommendations_complete(self):
        if self.rec1firstname and self.rec1lastname and self.rec1email and self.rec1phone and \
           self.rec1how and self.rec2firstname and self.rec2lastname and self.rec2email and \
           self.rec2phone and self.rec2how and self.rec3firstname and self.rec3lastname and \
           self.rec3email and self.rec3phone and self.rec3how:
           return True
        return False

    def are_recs_complete(self):
        recommenders_recommendations = Recommendation.query.filter_by(recommender_id = self.user_id).all()
        
        count_incompletes=0
        
        for r in recommenders_recommendations:
            if r.recommendation_complete == 0:
                count_incompletes += 1
                
                if count_incompletes == 0:
                    self.all_recs_complete = 1
                    db.session.add(self)
                    db.session.commit()
                    return True
                else:
                    self.all_recs_complete = 0
                    db.session.add(self)

            db.session.commit()
            return False

    def get_students(self):
        s = []
        applicant1 = User.query.filter_by(role = 1, rec1email = self.email).first()
        applicant2 = User.query.filter_by(role = 1, rec2email = self.email).first()
        applicant3 = User.query.filter_by(role = 1, rec3email = self.email).first()
        if applicant1:
            s.append(applicant1)
        if applicant2:
            s.append(applicant2)
        if applicant3:
            s.append(applicant3)
        students = [(User.query.get(1)),applicant3]
        return students

    def recommendation_is_complete_for(self, student):
        rec = Recommendation.query.filter_by(recommender_id = self.user_id, student_id = student.user_id).first()
        
        if rec.recommendation_complete ==1:
            return True
        else:
            return False

    def set_password(self, password):
        self.password = password
        db.session.add(self)
        db.session.commit()

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    recommender_id = db.Column(db.Integer)
    recq1 = db.Column(db.Integer)
    recq1ex = db.Column(db.Text)
    recq2 = db.Column(db.Integer)
    recq2ex = db.Column(db.Text)
    recq3 = db.Column(db.Integer)
    recq3ex = db.Column(db.Text)
    recq4 = db.Column(db.Integer)
    recq4ex = db.Column(db.Text)
    recq5 = db.Column(db.Integer)
    recq5ex = db.Column(db.Text)
    recq6 = db.Column(db.Integer)
    recq6ex = db.Column(db.Text)
    recq7 = db.Column(db.Text)
    recq8 = db.Column(db.Text)
    recommendation_complete = db.Column(db.Integer, default = 0)
    timestamp = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Recommendation %r>' % (self.id)
        
    def is_recommendation_complete(self):
        if self.recq1 and self.recq1ex and self.recq2 and self.recq2ex and self.recq3 and self.recq3ex and \
            self.recq4 and self.recq4ex and self.recq5 and self.recq5ex and self.recq6 and self.recq6ex and \
            self.recq7 and self.recq8:
            self.recommendation_complete = 1
            db.session.add(self)
            db.session.commit()
            return True
        return False
