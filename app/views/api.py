from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.utils import json_response
from app.utils.validators import validate_required_properties, validate_players_teams
from app.utils.validators import validate_players_inside_of_match, validate_player_inside_of_match
from app.models.fulboQL import Manager, Referee, Match, Team, Player, Club, Event, Foul
from app.models.fulboQL import Highlight, MatchMoment, OnGoal, Restart, Substitution, Injury
api_blueprint = Blueprint('api', __name__)

# referee
@api_blueprint.route('/api/referee/', methods=['GET', 'POST'])
@login_required
def referee():
    if request.method == 'POST':
        validate_required_properties(Referee, request)
        new_referee = Referee(name=(request.json['name']),
          surname=(request.json['surname']))
        db.session.add(new_referee)
        db.session.commit()
        return json_response(new_referee), 201
    query = db.session.query(Referee).all()
    return json_response(query), 200


@api_blueprint.route('/api/referee/<id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def refereeId(id):
    referee = db.session.query(Referee).filter(Referee.id == id)[0]
    if request.method == 'GET':
        return json_response(referee), 200
    if request.method == 'PUT':
        validate_required_properties(Referee, request)
        referee.name = request.json['name']
        referee.surname = request.json['surname']
        db.session.commit()
        return json_response(referee), 200
    if request.method == 'DELETE':
        db.session.delete(referee)
        db.session.commit()
        return jsonify({'message': 'referee deleted'}), 200


# manager
@api_blueprint.route('/api/manager/', methods=['GET', 'POST'])
@login_required
def manager():
    if request.method == 'POST':
        validate_required_properties(Manager, request)
        new_manager = Manager(
            name=(request.json['name']),
            surname=(request.json['surname']),
            club_id=(request.json['club']))
        db.session.add(new_manager)
        db.session.commit()
        return json_response(new_manager), 201
    query = db.session.query(Manager).all()
    return json_response(query), 200


@api_blueprint.route('/api/manager/<id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def managerId(id):
    manager = db.session.query(Manager).filter(Manager.id == id)[0]
    if request.method == 'GET':
        return json_response(manager), 200
    if request.method == 'PUT':
        validate_required_properties(Manager, request)
        manager.name = request.json['name']
        manager.surname = request.json['surname']
        manager.club_id = request.json['club']
        db.session.commit()
        return json_response(manager), 200
    if request.method == 'DELETE':
        db.session.delete(manager)
        db.session.commit()
        return jsonify({'message': 'manager deleted'}), 200


# club
@api_blueprint.route('/api/club/', methods=['GET', 'POST'])
@login_required
def club():
    if request.method == 'POST':
        validate_required_properties(Club, request)
        new_club = Club(name=(request.json['name']),
          stadium=(request.json['stadium']),
          city=(request.json['city']))
        db.session.add(new_club)
        db.session.commit()
        return json_response(new_club), 201
    query = db.session.query(Club).all()
    return json_response(query), 200


@api_blueprint.route('/api/club/<id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def clubId(id):
    club = db.session.query(Club).filter(Club.id == id)[0]
    if request.method == 'GET':
        return json_response(club), 200
    if request.method == 'PUT':
        validate_required_properties(Club, request)
        club.name = request.json['name']
        club.stadium = request.json['stadium']
        club.city = request.json['city']
        if 'players' in request.json:
            club_players = db.session.query(Player).filter(Player.id in request.json['Players'])
            for player in club_players:
                player.club_id = id
        db.session.commit()
        return json_response(club), 200
    if request.method == 'DELETE':
        db.session.delete(club)
        db.session.commit()
        return jsonify({'message': 'club deleted'}), 200


@api_blueprint.route('/api/club/<id>/addplayer/<player_id>/', methods=['PUT'])
@login_required
def club_add_player(id, player_id):
    club = db.session.query(Club).filter(Club.id == id)[0]
    player = db.session.query(Player).filter(Player.id == player_id)[0]
    if player.club_id != club.id:
        player.club_id = club.id
        db.session.commit()
        return json_response(club), 201
    else:
        return abort(400, "Player with id {} already belongs to that club.".format(player_id))


# player
@api_blueprint.route('/api/player/', methods=['GET', 'POST'])
@login_required
def player():
    if request.method == 'POST':
        validate_required_properties(Player,request)
        new_player = Player(name=(request.json['name']),
          surname=(request.json['surname']),
          position=(request.json['position']))
        if 'club' in request.json:
            new_player.club.id = request.json['club_id']
        db.session.add(new_player)
        db.session.commit()
        return json_response(new_player), 201
    query = db.session.query(Player).all()
    return json_response(query), 200


@api_blueprint.route('/api/player/<id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def playerId(id):
    player = db.session.query(Player).filter(Player.id == id)[0]
    if request.method == 'GET':
        return json_response(player), 200
    if request.method == 'PUT':
        validate_required_properties(Player,request)
        player.name = request.json['name']
        player.surname = request.json['surname']
        player.position = request.json['position']
        if 'club_id' in request.json:
            player.club_id = request.json['club_id']
        db.session.commit()
        return json_response(player), 200
    if request.method == 'DELETE':
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'player deleted'}), 200


# team
@api_blueprint.route('/api/team/', methods=['GET', 'POST'])
@login_required
def team():
    if request.method == 'POST':
        validate_required_properties(Team,request)
        club = db.session.query(Club).filter(Club.id == request.json['club'])[0]
        new_team = Team(club=(request.json['club']),
          manager=(request.json['manager']))
        titulars = filter(lambda x: x.id in request.json['titulars'], club.players)
        substitutes = filter(lambda x: x.id in request.json['substitutes'], club.players)
        for player in titulars:
            new_team.titulars.append(player)

        for player in substitutes:
            new_team.substitutes.append(player)

        db.session.add(new_team)
        db.session.commit()
        return json_response(new_team), 201
    query = db.session.query(Team).all()
    return json_response(query), 200


@api_blueprint.route('/api/team/<id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def teamId(id):
    team = db.session.query(Team).filter(Team.id == id)[0]
    if request.method == 'GET':
        return json_response(team), 200
    if request.method == 'PUT':
        validate_required_properties(Team,request)
        team.club = request.json['club']
        team.manager = request.json['manager']
        db.session.commit()
        return json_response(team), 200
    if request.method == 'DELETE':
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'team deleted'}), 200

# match
@api_blueprint.route('/api/match/', methods=['GET', 'POST'])
@login_required
def match():
    if request.method == 'POST':
        validate_required_properties(Match,request)
        new_match = Match(teamA=(request.json['teamA']),
          teamB=(request.json['teamB']),
          dateOfStart=(request.json['dateOfStart']),
          referee=(request.json['referee']))
        db.session.add(new_match)
        db.session.commit()
        return json_response(new_match), 201
    query = db.session.query(Match).all()
    return json_response(query), 200


@api_blueprint.route('/api/match/<id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def matchId(id):
    match = db.session.query(Match).filter(Match.id == id)[0]
    if request.method == 'GET':
        return json_response(match), 200
    if request.method == 'PUT':
        validate_required_properties(Match,request)
        match.teamA = request.json['teamA']
        match.teamB = request.json['teamB']
        match.dateOfStart = request.json['dateOfStart']
        match.referee = request.json['referee']
        db.session.commit()
        return json_response(match), 200
    if request.method == 'DELETE':
        db.session.delete(match)
        db.session.commit()
        return jsonify({'message': 'match deleted'}), 200


@api_blueprint.route('/api/match/<match_id>/events/')
@login_required
def events(match_id):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    return json_response(match.events), 200

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/foul/', methods=['POST'])
@login_required
def foul(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(Foul,request)
    new_foul = Foul(
        punishment=request.json["punishment"],
        foulType=request.json["foulType"],
        perpetrator_id=request.json["perpetrator_id"]
    )
    if "victim_id" in request.json:
        new_foul.victim_id = request.json["victim_id"]
    _, _, players = validate_players_inside_of_match(match, timestamp, new_foul.involved_players_ids())
    if len(new_foul.involved_players_ids()) > 1:
        validate_players_teams(players, different_teams=True)
    if "restart" in request.json:
        new_foul.restart = request.json["restart"]
    db.session.add(new_foul)
    new_event.foul = new_foul
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/highlight/', methods=['POST'])
@login_required
def highlight(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(Highlight,request)
    new_highlight = Highlight(
        description=request.json["description"]
    )
    players = db.session.query(Player).filter(Player.id.in_(request.json["players"])).all()
    validate_players_inside_of_match(match, timestamp, players)
    for player in players:
        new_highlight.players.append(player)
    db.session.add(new_highlight)
    new_event.highlight = new_highlight
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/matchmoment/', methods=['POST'])
@login_required
def matchmoment(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(MatchMoment,request)
    new_matchmoment = MatchMoment(
        momentType=request.json["momentType"]
    )
    db.session.add(new_matchmoment)
    new_event.matchmoment = new_matchmoment
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/ongoal/', methods=['POST'])
@login_required
def ongoal(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(OnGoal,request)
    new_ongoal = OnGoal(
        shooter_id=request.json["shooter_id"],
        goalkeeper_id=request.json["goalkeeper_id"],
        goal=request.json["goal"],
        penalty=request.json["penalty"]
    )
    if "assist_id" in request.json:
        new_ongoal.assist_id = request.json["assist_id"]
    _, _, players = validate_players_inside_of_match(match, timestamp, new_ongoal.involved_players_ids())
    shooter = list(filter(lambda p: p.id == request.json["shooter_id"], players))[0]
    goalkeeper = list(filter(lambda p: p.id == request.json["goalkeeper_id"], players))[0]
    validate_players_teams((shooter,goalkeeper),different_teams=True)
    if "assist_id" in request.json:
        assist = list(filter(lambda p: p.id == request.json["assist_id"], players))[0]
        validate_players_teams((shooter,assist),different_teams=False)
    db.session.add(new_ongoal)
    new_event.ongoal = new_ongoal
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/restart/', methods=['POST'])
@login_required
def restart(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(Restart,request)
    validate_player_inside_of_match(match, timestamp, request.json["executor_id"])
    new_restart = Restart(
        restartType=request.json["restartType"],
        executor_id=request.json["executor_id"]
    )
    db.session.add(new_restart)
    new_event.restart = new_restart
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/substitution/', methods=['POST'])
@login_required
def substitution(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(Substitution,request)
    _, teams, player_out = validate_player_inside_of_match(match, timestamp, request.json["outPlayer_id"])
    _, _, player_in = validate_player_inside_of_match(match, timestamp, request.json["inPlayer_id"], as_substitute=True, teams=teams)
    validate_players_teams((player_in,player_out),different_teams=False)
    new_substitution = Substitution(
        inPlayer_id=request.json["inPlayer_id"],
        outPlayer_id=request.json["outPlayer_id"]
    )
    db.session.add(new_substitution)
    new_event.substitution = new_substitution
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201

@api_blueprint.route('/api/match/<match_id>/events/<timestamp>/injury/', methods=['POST'])
@login_required
def injury(match_id, timestamp):
    match = db.session.query(Match).filter(Match.id == match_id)[0]
    new_event = Event(
        timestamp=timestamp,
        reportedBy=current_user.id,
        match=match_id
    )
    validate_required_properties(Injury,request)
    validate_player_inside_of_match(match, timestamp, request.json["injured_id"])
    new_injury = Injury(
        injured_id=request.json["injured_id"],
        severity=request.json["severity"]
    )
    if "substitution_id" in request.json:
        new_injury.substitution_id = request.json["substitution_id"]
    db.session.add(new_injury)
    new_event.injury = new_injury
    db.session.add(new_event)
    db.session.commit()
    return json_response(new_event), 201