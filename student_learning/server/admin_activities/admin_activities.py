#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 04:56:19 2020

@author: gauravsingh
"""

from flask import Blueprint, render_template,request,make_response, jsonify

from student_learning.server.models import User, Assigned_Classes,Questions,AllClasses


from student_learning.server import db


from flask.views import MethodView


admin_blueprint = Blueprint('admin_blueprint', __name__)


class AssignClassesAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        
        requested_questions = post_data.get("questions")
        try:
            
            question_ids = []
            for question in list(requested_questions):
                question_id = Questions.query.filter_by(questions= question).first()
                question_ids.append(question_id)
            requested_classes = post_data.get("classes")
            class_ids = []
            for classs in list(requested_classes):
                class_id = AllClasses.query.filter_by(classes= classs).first()
                class_ids.append(class_id)
                
            user_id = User.query.filter_by(name = post_data.get("name")).first()
            
            assigned_classes = Assigned_Classes(user_id.id,str(class_ids),str(question_ids))
            db.session.add(assigned_classes)
            db.session.commit()
            responseObject = {
                        'status': 'success',
                        'message': 'Classes and Questions assigned.'
                        
                    }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            
            responseObject = {
                 
                'status': 'fail',
                'message': ' Could Not Assign.'
            }
            return make_response(jsonify(responseObject)), 401
        



        
assign_classes_view = AssignClassesAPI.as_view('assign_classes')


admin_blueprint.add_url_rule(
    '/assign_classes',
    view_func=assign_classes_view,
    methods=['POST']
)        
        
        
        
 









