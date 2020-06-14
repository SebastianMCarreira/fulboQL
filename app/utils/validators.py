from flask import abort
from app import db
from app.models.fulboQL import Manager, Referee, Match, Team, Player, Club, Event, Foul
from app.models.fulboQL import Highlight, MatchMoment, OnGoal, Restart, Substitution, Injury
from app.models.timestamp import TimeStamp

def validate_required_properties(cls, request):
    if not cls.verifyProperties(request.json):
        return abort(400, "Required properties: "+", ".join(cls.required_properties))

def validate_players_inside_of_match(match, timestamp, players, teams=None):
    if type(match) is int:
        match = Match.query.filter(Match.id == match).first()
    if type(players[0]) is int:
        players = Player.query.filter(Player.id.in_(players))
    if not teams:
        teams = Team.query.filter(Team.id.in_((match.teamA,match.teamB)))
    for player in players:
        validate_player_inside_of_match(match, timestamp, player, teams=teams)

def validate_player_inside_of_match(match, timestamp, player, teams=None):
    if type(match) is int:
        match = Match.query.filter(Match.id == match).first()
    if type(player) is int:
        player = Player.query.filter(Player.id == player).first()
    if not teams:
        teams = Team.query.filter(Team.id.in_((match.teamA,match.teamB)))

    team = None
    if player.club_id == teams[0].club:
        team = teams[0]
    elif player.club_id == teams[1].club:
        team = teams[1]
    else:
        abort(400, "The player with id {} does not belong to any club in the match with id {}".format(player.id, match.id))
     
    if player not in team.players:
        abort(400, "The player with id {} was not listed as titular or substitue in the team with id {}".format(player.id, team.id))
    
    substitutions = sorted(filter(
                    lambda event: event.substitution is not None and 
                        event.substitution.outPlayer_id in [player.id for player in team.players] and
                        TimeStamp(event.timestamp) < TimeStamp(timestamp),
                    match.events))
    field_players_ids = [player.id for player in team.titulars]
    for substitution in substitutions:
        field_players_ids.remove(substitution.substitution.outPlayer_id)
        field_players_ids.append(substitution.substitution.inPlayer_id)
    if player.id not in field_players_ids:
        abort(400,"The player with id {} was at the substitute bank at the timestamp {}".format(player.id, timestamp))
        

    

    
