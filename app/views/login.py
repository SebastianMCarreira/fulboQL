from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_user import current_user, roles_required
from flask_login import login_user, login_required
from app import db
from app.utils import json_response
from app.models.fulboQL import Manager, Referee, Match, Team, Player, Club, Event, Foul
from app.models.fulboQL import Highlight, MatchMoment, OnGoal, Restart, Substitution, Injury
from app.security import get_user_from_credentials
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/login/", methods=["POST"])
def login():
    user = get_user_from_credentials(request.json["username"],request.json["password"])
    if user:
        login_user(user)
        return "OK"
    else:
        abort(403)
