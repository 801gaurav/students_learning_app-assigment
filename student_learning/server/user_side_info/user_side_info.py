#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 05:44:31 2020

@author: gauravsingh
"""

from flask import Blueprint, render_template,request,make_response, jsonify

from student_learning.server.models import User, Assigned_Classes,Questions,AllClasses

from student_learning.server import db


from flask.views import MethodView


user_side_info_blueprint = Blueprint('user_side_info_blueprint', __name__)


class GetAssignedClassesAPI(MethodView):
    def get(self):
        user_id = request.headers.get('id')
        try:
            
            
            all_details = Assigned_Classes.query.filter_by(user_id=user_id).first()
            questions = Questions.query.filter_by(all_details.questions).first()
            classes = AllClasses.query.filter_by(all_details.classes).first()
            responseObject = {
                        'status': 'success',
                        'data':{'questions':questions,'classes':classes}
                        
                    }
            return make_response(jsonify(responseObject)), 200
        
        
        except Exception as e:
            
            responseObject = {
                 
                'status': 'fail',
                'message': ' No Questions or Classes found.'
            }
            return make_response(jsonify(responseObject)), 400
    
        

        
get_assign_classes = GetAssignedClassesAPI.as_view('get_assign_classes')


user_side_info_blueprint.add_url_rule(
    '/class_details',
    view_func=get_assign_classes,
    methods=['GET']
)        
         
    
    