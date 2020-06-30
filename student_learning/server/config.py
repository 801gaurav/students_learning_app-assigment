#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 01:18:16 2020

@author: gauravsingh
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))



class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', b'M\x93\x8d\xa3\xf0\xd3\xdfCaS\xea\x95\x9e=\xb2\x1c\xdb\x9e\x16\x02:\x95\x08\xa4')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class Config(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")