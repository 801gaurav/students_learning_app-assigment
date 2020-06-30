#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 23:53:11 2020

@author: gauravsingh
"""

from flask import Blueprint, render_template,request,make_response, jsonify

from student_learning.server.models import User, BlacklistToken

from student_learning.server import app,db,bcrypt

from flask.views import MethodView


auth_blueprint = Blueprint('auth_blueprint', __name__)



@auth_blueprint.route("/")
def home_page():
    return render_template("login_page.html")



class RegisterAPI(MethodView):
    

    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    name=post_data.get('name'),
                    age=post_data.get('age'),
                    city=post_data.get('city'),
                    grade_of_study=post_data.get('grade_of_study'),
                    board_of_study=post_data.get('board_of_study')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            
            return make_response(jsonify(responseObject)), 202
        
        
        
        
registration_view = RegisterAPI.as_view('register_api')


auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)        
        
        
        
        
        
        
        
        