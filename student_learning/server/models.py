#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 01:52:35 2020

@author: gauravsingh
"""
import jwt
import datetime

from student_learning.server import app,db,bcrypt


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    name = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    age = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    city = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    
    grade_of_study = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    board_of_study = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    
    
    registered_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    
    def __init__(self, email, name,age,city,password,grade_of_study,board_of_study, admin=False):
        self.email = email
        self.name = name
        self.age = age
        self.city=city
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.grade_of_study= grade_of_study
        self.board_of_study= board_of_study
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    
    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
        
class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
        
        
class All_Grades(db.Model):
    __tablename__ = 'all_grades'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    grade = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    
    def __init__(self,grade):
        self.grade = grade
        
        
        
        
class AllClasses(db.Model):
    __tablename__= "allclasses"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    classes = db.Column(
        db.String(200),
        index=False,
        unique=True,
        nullable=False
    )
    
    
class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    questions = db.Column(
        db.String(200),
        index=False,
        unique=True,
        nullable=False
    )
    
    def __init__(self,questions):
        self.questions = questions
        
class Assigned_Classes(db.Model):
    __tablename__ = 'assigned_classes'
    user_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    classes_ids = db.Column(
        db.String(200),
        index=False,
        unique=True,
        nullable=False
    )
    questions_ids = db.Column(
        db.String(200),
        index=False,
        unique=True,
        nullable=False
    )
    
    def __init__(self,user_id,classes_ids,questions_ids):
        self.user_id = user_id
        self.classes_ids=classes_ids
        self.questions_ids=questions_ids
        
    
    