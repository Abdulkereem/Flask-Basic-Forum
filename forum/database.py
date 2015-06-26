from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forum import app
db = SQLAlchemy(app)
import re

password_regex = re.compile("^[a-zA-Z0-9!@#%&]{6,40}$")
username_regex = re.compile("^[a-zA-Z0-9!@#%&]{4,40}$")
#Account checks
def username_taken(username):
	return User.query.filter(User.username == username).first()
def email_taken(email):
	return User.query.filter(User.email == email).first()
def valid_username(username):
	if not username_regex.match(username):
		#username does not meet password reqirements
		return False
	#username is not taken and does meet the password requirements
	return True
def valid_password(password):
	return password_regex.match(password)
#Post checks
def valid_title(title):
	return len(title) > 4 and len(title) < 140
def valid_content(content):
	return len(content) > 10 and len(content) < 5000


#OBJECT MODELS
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, unique=True)
	password_hash = db.Column(db.Text)
	email = db.Column(db.Text, unique=True)
	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	content = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	subforum_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
	def __init__(self, title, content, poster):
		self.title = title
		self.content = content
		self.user_id = poster.id
	def get_user(self):
		return User.query.filter(User.id == self.user_id).first()
class Subforum(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text, unique=True)
	description = db.Column(db.Text)
	posts = db.relationship("Post", backref="subforum")
	def __init__(self, title, description):
		self.title = title
		self.description = description
def get_poster(post):
	return User.query.filter(User.id == post.user_id).first()
