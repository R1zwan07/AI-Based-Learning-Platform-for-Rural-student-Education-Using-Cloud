# models.py
from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    # This is a placeholder; you'll need to differentiate between user types
    return Student.query.get(int(user_id)) or Faculty.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    # Admin model with credentials. Only one admin would be needed, or you could have multiple.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Faculty(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    materials = db.relationship('Material', backref='author', lazy=True)

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    materials = db.relationship('Material', backref='subject', lazy=True)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(20), nullable=False) # 'video', 'youtube', 'pdf'
    url = db.Column(db.String(200), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)