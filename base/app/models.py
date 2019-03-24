from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    usertype = db.Column(db.String(64),unique=False, nullable=False)
    nricHash = db.Column(db.String(128))
    points = db.Column(db.Integer, unique=False, nullable=True, default=0)
    passwordHash = db.Column(db.String(128))
    # question = db.relationship("Question", backref="question", uselist=True, cascade='all')
    # response = db.relationship("Response", backref="user", uselist=True, cascade='all')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def set_nric(self, nric):
        self.nricHash = generate_password_hash(nric)

    def check_nric(self, nric):
        return check_password_hash(self.nricHash, nric)


    def serialize(self):
        return {
            'username': self.username,
            'points': self.points,
            'usertype': self.userType
            }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    questionTitle= db.Column(db.Text(), unique=False, nullable=False)
    questionOption= db.Column(db.Text(), unique=False, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    questionType = db.Column(db.String(64), unique=False, nullable=False)
    dateTime = db.Column(db.DateTime, unique=False, index=True, default=datetime.utcnow)

    # response = db.relationship("Response", backref="qn", uselist=True, cascade='all')
    def serialize(self):
        return {
            'questionID': self.id,
            'question': self.questionTitle
            }

class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    question = db.Column(db.Integer, db.ForeignKey("question.id"), unique=False, nullable=False)
    response = db.Column(db.Text(), index=True, unique=False, nullable=False)
    dateTime = db.Column(db.DateTime, unique=False, index=True, default=datetime.utcnow)

    def serialize(self):
        return {
            'userID': self.user,
            'questionID': self.questionTitle,
            'responseID': self.id,
            'response' : self.response
            }
