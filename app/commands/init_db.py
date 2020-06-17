# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role
from app.models.fulboQL import *
from app.security import generate_new_user, find_or_create_role

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    user_role = find_or_create_role('user', u'User')

    # Add users
    # Admin
    generate_new_user(
        current_app.config["INITIAL_USERS"]["admin"]["username"],
        current_app.config["INITIAL_USERS"]["admin"]["password"],
        current_app.config["INITIAL_USERS"]["admin"]["email"],
        current_app.config["INITIAL_USERS"]["admin"]["fname"],
        current_app.config["INITIAL_USERS"]["admin"]["lname"], 
        role=admin_role)
    # Normal user
    generate_new_user(
        current_app.config["INITIAL_USERS"]["user"]["username"],
        current_app.config["INITIAL_USERS"]["user"]["password"],
        current_app.config["INITIAL_USERS"]["user"]["email"],
        current_app.config["INITIAL_USERS"]["user"]["fname"],
        current_app.config["INITIAL_USERS"]["user"]["lname"])

    # Save to DB
    db.session.commit()





def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user



