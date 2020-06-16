from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_models import User, Role
from app import db
from app import login
from .email import send_activation_email
from .exceptions import InvalidCredentialsException, UsernameNotFoundException
import os

def generate_new_user(username, password, email, first_name, last_name, role=None):
    '''
        Generates a new user in the database with the given password hashed, the email
        confirmation token generated and sends the email with the token.
    '''
    if not role:
        role = find_or_create_role('user', u'User')

    password_hash = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        email_confirmation_token=os.urandom(32).hex(),
        email_confirmed=False,
        active=True,
        password=password_hash,
        first_name=first_name,
        last_name=last_name,
        roles=[role]
    )
    db.session.add(new_user)
    db.session.commit()
    send_activation_email(new_user)

def check_email_activation(user, activation_code):
    '''
        Verifies that the received activation token is valid and if it is, sets the email_confirmed
        flag as True in the db.
    '''
    if user.email_confirmation_token == activation_code:
        user.email_confirmed = True
        db.session.commit()
        return True
    else:
        return False

def change_password(user, old_password, new_password):
    if check_user_credentials(user, old_password):
        new_password_hash = generate_password_hash(new_password)
        user.password = new_password_hash
    else:
        raise InvalidCredentialsException("Username/Password invalid.")

def change_email(user, new_email):
    user.email = new_email
    user.email_confirmed = False
    user.email_confirmation_token = os.urandom(32).hex()
    db.session.commit()
    send_activation_email(user)

def change_name(user, first_name, last_name):
    user.first_name = first_name
    user.last_name = last_name
    db.session.commit()

def check_user_credentials(user, password):
    return check_password_hash(user.password, password)

def check_username_availability(username):
    if db.session.query(User).filter(User.username == username):
        return False
    else:
        return True

def check_email_availability(email):
    if db.session.query(User).filter(User.email == email):
        return False
    else:
        return True

def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
        db.session.commit()
    return role

def get_user_from_credentials(username, password):
    '''
        Verifies that the given credentials are valid and if they are, returns the
        corresponding user object.
    '''
    user = User.query.filter(User.username == username).first()
    if check_user_credentials(user, password):
        return user
    else:
        return None

@login.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

