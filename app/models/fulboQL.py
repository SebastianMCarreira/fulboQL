from enum import Enum
from app import db
from app.models.user_models import User
from .timestamp import TimeStamp

class ApiModel():
    required_properties = []
    @classmethod
    def verifyProperties(cls, content):
        return all([x in content for x in cls.required_properties])

class Person():
    @property
    def full_name(self):
        return "{} {}".format(self.name, self.surname)

class Club(db.Model, ApiModel):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False, server_default=u'')
    full_name = db.Column(db.String(64), nullable=False, server_default=u'')
    acronym = db.Column(db.String(16), nullable=False, server_default=u'')
    stadium = db.Column(db.Unicode(64), server_default=u'')
    city = db.Column(db.Unicode(64), server_default=u'')
    players = db.relationship('Player')
    manager = db.relationship("Manager", uselist=False, back_populates="club")

    required_properties = ["name","stadium","city","full_name","acronym"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'full_name': self.full_name,
            'acronym': self.acronym,
            'stadium': self.stadium,
            'city': self.city,
            'manager': self.manager.serialized if self.manager else None
        }

class Manager(db.Model, ApiModel, Person):
    __tablename__ = 'managers'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'')  
    surname = db.Column(db.String(50), nullable=False, server_default=u'')
    club_id = db.Column(db.Integer(), db.ForeignKey('clubs.id'))
    club = db.relationship("Club", back_populates="manager")

    required_properties = ["name","surname","club"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'club': self.club_id
        }


class Referee(db.Model, ApiModel, Person):
    __tablename__ = 'referees'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'')  
    surname = db.Column(db.String(50), nullable=False, server_default=u'')

    required_properties = ["name","surname"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname
        }


class PlayerPositions(str, Enum):
    GOALKEEPER = "GOALKEEPER"
    DEFENSE = "DEFENSE"
    MIDFIELDER = "MIDFIELDER"
    FORWARD = "FORWARD"

class Player(db.Model, ApiModel, Person):
    __tablename__ = 'players'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'')  
    surname = db.Column(db.String(50), nullable=False, server_default=u'')
    position = db.Column(db.Enum(PlayerPositions))
    club_id = db.Column(db.Integer(), db.ForeignKey('clubs.id'))
    club = db.relationship('Club')

    required_properties = ["name","surname","position"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'position': self.position,
            'club': self.club.serialized if self.club else None
        }

class PlayersTeams(db.Model):
    __tablename__ = 'players_teams'
    id = db.Column(db.Integer(), primary_key=True)
    player_id = db.Column(db.Integer(), db.ForeignKey('players.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))

class PlayersTeamsSubs(db.Model):
    __tablename__ = 'players_teams_substitutes'
    id = db.Column(db.Integer(), primary_key=True)
    player_id = db.Column(db.Integer(), db.ForeignKey('players.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))

class Team(db.Model, ApiModel):
    __tablename__ = 'teams'
    id = db.Column(db.Integer(), primary_key=True)
    club_id = db.Column(db.Integer(), db.ForeignKey('clubs.id'))
    club = db.relationship("Club")
    manager = db.Column(db.Integer(), db.ForeignKey('managers.id'))
    titulars = db.relationship('Player', secondary='players_teams')
    substitutes = db.relationship('Player', secondary='players_teams_substitutes')

    @property
    def players(self):
        return self.titulars + self.substitutes

    required_properties = ["club","manager","titulars","substitutes"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'club': self.club.serialized,
            'manager': self.manager,
        }

class Match(db.Model, ApiModel):
    __tablename__ = 'matches'
    id = db.Column(db.Integer(), primary_key=True)
    teamA = db.Column(db.Integer(), db.ForeignKey('teams.id'))
    teamB = db.Column(db.Integer(), db.ForeignKey('teams.id'))
    dateOfStart = db.Column(db.DateTime())
    referee_id = db.Column(db.Integer(), db.ForeignKey('referees.id'))
    referee = db.relationship('Referee')
    events = db.relationship('Event')
    closed = db.Column(db.Boolean(), default=False)

    required_properties = ["teamA","teamB","dateOfStart","referee_id"]
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'teamA': self.team_A.serialized,
            'teamB': self.team_B.serialized,
            'dateOfStart': self.dateOfStart.strftime("%Y/%m/%d %H:%M"),
            'referee': self.referee.serialized,
            'closed': self.closed,
            'canLoadMoreEvents': self.can_log_more_events(),
            'result': self.result
        }

    @property
    def team_A(self):
        return db.session.query(Team).filter(Team.id==self.teamA)[0]
    
    @property
    def team_B(self):
        return db.session.query(Team).filter(Team.id==self.teamB)[0]

    def can_log_more_events(self):
        second_extra_end_event = list(filter(
            lambda event: event.matchmoment is not None and 
            event.matchmoment.momentType is MatchMomentType.SECONEXTRAEND,self.events))
        if second_extra_end_event:
            return False
        return True

    @property
    def result(self):
        teamAGoals = 0
        teamBGoals = 0
        for event in self.events:
            if event.ongoal and event.ongoal.serialized["goal"]:
                if event.ongoal.serialized["shooter"]["club"]["id"] == self.team_A.club_id:
                    teamAGoals += 1
                elif event.ongoal.serialized["shooter"]["club"]["id"] == self.team_B.club_id:
                    teamBGoals += 1
                else:
                    print("wat??")
        return {
            'teamA': teamAGoals,
            'teamB': teamBGoals
        }

class Event(db.Model, ApiModel):
    __tablename__ = 'events'
    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.String(9))
    reportedBy = db.Column(db.Integer(), db.ForeignKey('users.id'))
    match = db.Column(db.Integer(), db.ForeignKey('matches.id'))
    foul_id = db.Column(db.Integer(), db.ForeignKey('fouls.id'))
    foul = db.relationship("Foul", uselist=False)
    highlight_id = db.Column(db.Integer(), db.ForeignKey('highlights.id'))
    highlight = db.relationship("Highlight", uselist=False)
    matchMoment_id = db.Column(db.Integer(), db.ForeignKey('matchmoments.id'))
    matchmoment = db.relationship("MatchMoment", uselist=False)
    onGoal_id = db.Column(db.Integer(), db.ForeignKey('ongoals.id'))
    ongoal = db.relationship("OnGoal", uselist=False)
    restart_id = db.Column(db.Integer(), db.ForeignKey('restarts.id'))
    restart = db.relationship("Restart", uselist=False)
    substitution_id = db.Column(db.Integer(), db.ForeignKey('substitutions.id'))
    substitution = db.relationship("Substitution", uselist=False)
    injury_id = db.Column(db.Integer(), db.ForeignKey('injuries.id'))
    injury = db.relationship("Injury", uselist=False)

    required_properties = ["timestamp","reportedBy","match"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        output = {
            'id': self.id,
            'timestamp': self.timestamp,
            'reportedBy': self.reportedBy,
            'match': self.match
        }
        if self.foul:
            output["foul"] = self.foul.serialized
        if self.highlight:
            output["highlight"] = self.highlight.serialized
        if self.matchmoment:
            output["matchmoment"] = self.matchmoment.serialized
        if self.ongoal:
            output["ongoal"] = self.ongoal.serialized
        if self.restart:
            output["restart"] = self.restart.serialized
        if self.substitution:
            output["substitution"] = self.substitution.serialized
        if self.injury:
            output["injury"] = self.injury.serialized
        return output

    def __lt__(a,b):
        return TimeStamp(a.timestamp) < TimeStamp(b.timestamp)
    
    def __gt__(a,b):
        return TimeStamp(a.timestamp) > TimeStamp(b.timestamp)

    def __eq__(a,b):
        return TimeStamp(a.timestamp) == TimeStamp(b.timestamp)

class FoulPunishments(str, Enum):
    NONE = "NONE"
    WARNING = "WARNING"
    YELLOW = "YELLOW"
    RED = "RED"

class FoulTypes(str, Enum):
    HAND = "HAND"
    VIOLENTKICK = "VIOLENTKICK"
    OTHERVIOLENCE = "OTHERVIOLENCE"
    HOLDPLAYER = "HOLDPLAYER"
    CHARGEPLAYER = "CHARGEPLAYER"
    BACKPASS = "BACKPASS"
    REFEREEINSULT = "REFEREEINSULT"
    OFFSIDE = "OFFSIDE"

class Foul(db.Model, ApiModel):
    __tablename__ = 'fouls'
    id = db.Column(db.Integer(), primary_key=True)
    punishment = db.Column(db.Enum(FoulPunishments))
    foulType = db.Column(db.Enum(FoulTypes))
    perpetrator_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    victim_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    restart = db.Column(db.Integer(), db.ForeignKey('restarts.id'))

    required_properties = ["punishment","foulType","perpetrator_id"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'punishment': self.punishment,
            'foulType': self.foulType,
            'perpetrator': db.session.query(Player).filter(Player.id==self.perpetrator_id)[0].serialized,
            'victim': db.session.query(Player).filter(Player.id==self.victim_id)[0].serialized if self.victim_id else None
        }
    
    def involved_players_ids(self):
        involved_players = [self.perpetrator_id]
        if self.victim_id:
            involved_players.append(self.victim_id)
        return involved_players

class HighlightsPlayers(db.Model, ApiModel):
    __tablename__ = 'highlights_players'
    id = db.Column(db.Integer(), primary_key=True)
    player_id = db.Column(db.Integer(), db.ForeignKey('players.id', ondelete='CASCADE'))
    highlight_id = db.Column(db.Integer(), db.ForeignKey('highlights.id', ondelete='CASCADE'))

class Highlight(db.Model, ApiModel):
    __tablename__ = 'highlights'
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(1024))
    players = db.relationship("Player", secondary="highlights_players")

    required_properties = ["description", "players"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'description': self.description,
            'players': [player.serialized for player in self.players]
        }


class MatchMomentType(str, Enum):
    FIRSTTIMESTART = "FIRSTTIMESTART"   # 0 
    FIRSTTIMEEND = "FIRSTTIMEEND"       # 1
    SECONTIMESTART = "SECONTIMESTART"   # 2
    SECONTIMEEND = "SECONTIMEEND"       # 3
    FIRSTEXTRASTART = "FIRSTEXTRASTART" # 4
    FIRSTEXTRAEND = "FIRSTEXTRAEND"     # 5
    SECONEXTRASTART = "SECONEXTRASTART" # 6
    SECONEXTRAEND = "SECONEXTRAEND"     # 7

class MatchMoment(db.Model, ApiModel):
    __tablename__ = 'matchmoments'
    id = db.Column(db.Integer(), primary_key=True)
    momentType = db.Column(db.Enum(MatchMomentType))
    
    required_properties = ["momentType"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'momentType': self.momentType
        }

class OnGoal(db.Model, ApiModel):
    __tablename__ = 'ongoals'
    id = db.Column(db.Integer(), primary_key=True)
    shooter_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    assist_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    goalkeeper_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    goal = db.Column(db.Boolean())
    penalty = db.Column(db.Boolean())

    required_properties = ["shooter_id","goalkeeper_id","goal","penalty"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'shooter': db.session.query(Player).filter(Player.id==self.shooter_id)[0].serialized,
            'assist': db.session.query(Player).filter(Player.id==self.assist_id)[0].serialized if self.assist_id else None,
            'goalkeeper': db.session.query(Player).filter(Player.id==self.goalkeeper_id)[0].serialized,
            'goal': self.goal,
            'penalty': self.penalty
        }

    def involved_players_ids(self):
        involved_players = [self.shooter_id, self.goalkeeper_id]
        if self.assist_id:
            involved_players.append(self.assist_id)
        return involved_players

class RestartTypes(str, Enum):
    FREEKICK = "FREEKICK"
    PENALTY = "PENALTY"
    GOALKICK = "GOALKICK"
    DROPBALL = "DROPBALL"
    CORNER = "CORNER"
    KICKOFF = "KICKOFF"
    THROWIN = "THROWIN"

class Restart(db.Model, ApiModel):
    __tablename__ = 'restarts'
    id = db.Column(db.Integer(), primary_key=True)
    restartType = db.Column(db.Enum(RestartTypes))
    executor_id = db.Column(db.Integer(), db.ForeignKey('players.id'))

    required_properties = ["restartType","executor_id"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'restartType': self.restartType,
            'executor': db.session.query(Player).filter(Player.id==self.executor_id)[0].serialized
        }

class Substitution(db.Model, ApiModel):
    __tablename__ = 'substitutions'
    id = db.Column(db.Integer(), primary_key=True)
    inPlayer_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    outPlayer_id = db.Column(db.Integer(), db.ForeignKey('players.id'))

    required_properties = ["inPlayer_id","outPlayer_id"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'inPlayer': db.session.query(Player).filter(Player.id==self.inPlayer_id)[0].serialized,
            'outPlayer': db.session.query(Player).filter(Player.id==self.outPlayer_id)[0].serialized
        }

class InjurySeverity(str, Enum):
    LOW = "LOW" # The player could continue playing normally
    MED = "MED" # The player could continue playing with some difficulty
    HIG = "HIG" # The player could continue playing with high difficulty
    OUT = "OUT" # The player could not continue playing

class Injury(db.Model, ApiModel):
    __tablename__ = 'injuries'
    id = db.Column(db.Integer(), primary_key=True)
    injured_id = db.Column(db.Integer(), db.ForeignKey('players.id'))
    severity = db.Column(db.Enum(InjurySeverity))
    substitution_id = db.Column(db.Integer(), db.ForeignKey('substitutions.id'))

    required_properties = ["injured_id","severity"]

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'injured': db.session.query(Player).filter(Player.id==self.injured_id)[0].serialized,
            'severity': self.severity,
            'substitution': db.session.query(Substitution).filter(Substitution.id==self.substitution_id)[0].serialized if self.substitution_id else None
        }