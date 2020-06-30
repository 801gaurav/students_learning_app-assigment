#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 01:06:49 2020

@author: gauravsingh
"""


import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

# app_settings = os.getenv(
#     'APP_SETTINGS',
#     'config.Config'
# ) 
app.config.from_object('student_learning.server.config.Config')

bcrypt = Bcrypt(app)
db = SQLAlchemy()
db.init_app(app)
#db.create_all()

from student_learning.server.auth.auth import auth_blueprint
app.register_blueprint(auth_blueprint)

from student_learning.server.admin_activities.admin_activities import admin_blueprint

app.register_blueprint(admin_blueprint)


