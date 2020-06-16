from flask import abort
from app import db
from app.models.fulboQL import Manager, Referee, Match, Team, Player, Club, Event, Foul
from app.models.fulboQL import Highlight, MatchMoment, OnGoal, Restart, Substitution, Injury
from app.models.timestamp import TimeStamp

def validate_required_properties(cls, request):
    '''
        Validates that the request received has all of the properties required to
        create the given object.
    '''
    if not cls.verifyProperties(request.json):
        return abort(400, "Required properties: "+", ".join(cls.required_properties))

def validate_players_inside_of_match(match, timestamp, players, teams=None):
    '''
        Validates that a list of players was present inside of the match (not in the
        substitutes bench) at the given timestamp.
        The parameters match, players and teams can be either the ids of the corresponding
        objects (which will be searched in the DB to be converted to the objects) or the
        objects themselves if the code that invoked this function already had access to
        them to prevent unnecessary queries.
    '''
    if type(match) is int:
        match = Match.query.filter(Match.id == match).first()
    if type(players[0]) is int:
        players = Player.query.filter(Player.id.in_(players))
    if not teams:
        teams = Team.query.filter(Team.id.in_((match.teamA,match.teamB)))
    for player in players:
        validate_player_inside_of_match(match, timestamp, player, teams=teams)
    return match, teams, players

def validate_player_inside_of_match(match, timestamp, player, teams=None, as_substitute=False):
    '''
        Validates that a given player was present in the match at the given timestamp (either
        at the substitute bench or inside the field).
        The parameters match, player and teams can be either the ids of the corresponding
        objects (which will be searched in the DB to be converted to the objects) or the
        objects themselves if the code that invoked this function already had access to
        them to prevent unnecessary queries.
    '''
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
    bench_players_ids = [player.id for player in team.substitutes]
    for substitution in substitutions:
        field_players_ids.remove(substitution.substitution.outPlayer_id)
        field_players_ids.append(substitution.substitution.inPlayer_id)
        bench_players_ids.remove(substitution.substitution.inPlayer_id)
        bench_players_ids.append(substitution.substitution.outPlayer_id)
    
    if player.id not in field_players_ids and not as_substitute:
        abort(400,"The player with id {} was at the substitute bench at the timestamp {}".format(player.id, timestamp))
    elif player.id not in bench_players_ids and as_substitute:
        abort(400,"The player with id {} was inside of the field at the timestamp {}".format(player.id, timestamp))
    return match, teams, player

def validate_players_teams(players, different_teams=False):
    '''
        Validates that two players belong to either the same team or different teams (as decided by
        the different_teams flag).
    '''
    if len(players) != 2:
        raise ValueError("The players touple must have exactly 2 items.")
    if type(players[0]) is int:
        players = Player.query.filter(Player.id.in_(players))
    if different_teams and players[0].club_id == players[1].club_id:
        abort(400,"Players with ids {} and {} belong to the same team.".format(players[0].id,players[1].id))
    elif not different_teams and players[0].club_id != players[1].club_id:
        abort(400,"Players with ids {} and {} belong to different team.".format(players[0].id,players[1].id))
    return players
