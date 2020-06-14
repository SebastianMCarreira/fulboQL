import re
from flask import abort

def validate_timestamp(timestamp):
    pattern = re.compile("\d{1,3}(\+\d+)?:[0-5]\d")
    if not pattern.match(timestamp):
        abort(400, "The timestamp is invalid.")

class TimeStamp():
    '''
        A timestamp must be composed of:
            - the number of minutes of the match (1 to 3 digits) without leading zeroes. Ex: 45
            - followed by a + and the minutes that have passed since the time should have 
              ended (if the time's minutes have already passed). Ex: +2
            - followed by a :
            - followed by the number of seconds since the minute started with one leading zero. Ex: 02
        Examples:
            - Minute 2 of the first time at 20 seconds:     2:20
            - Minute 47 of the first time at 5 seconds:     45+2:05
            - Minute 2 of the second time at 50 seconds:    47:50
            - Minute 45 of the second time at 1 second:     90+0:01
            - Minute 0 of the first extra time at 1 second: 90:01
            - Other examples sorted:
                '0:41 ',
                '2:20',
                '45+0:45',
                '45+2:05',
                '45+2:14',
                '45:20',
                '47:50',
                '70:26',
                '89:44',
                '90+0:00',
                '90+0:01',
                '90+1:11',
                '90+5:16',
                '90:00',
                '90:01'
    '''
    def __init__(self, timestamp):
        validate_timestamp(timestamp)
        self.timestamp = timestamp
        self.seconds = int(timestamp.split(":")[1])
        minutes = timestamp.split(":")[0]
        if "+" in minutes:
            time_minutes = int(minutes.split("+")[0])
            extra_minutes = int(minutes.split("+")[1])
            if time_minutes <= 45:
                self.time = 1
            elif time_minutes <= 90:
                self.time = 2
            elif time_minutes <= 105:
                self.time = 3
            else:
                self.time = 4
            self.minutes = time_minutes + extra_minutes
        else:
            minutes = int(minutes)
            if minutes < 45:
                self.time = 1
            elif minutes < 90:
                self.time = 2
            elif minutes < 105:
                self.time = 3
            else:
                self.time = 4
            self.minutes = minutes

    def __lt__(self, b):
        if self.time < b.time:
            return True
        if self.time > b.time:
            return False
        if self.minutes < b.minutes:
            return True
        if self.minutes > b.minutes:
            return False
        return self.seconds < b.seconds

    def __gt__(self, b):
        if self.time > b.time:
            return True
        if self.time < b.time:
            return False
        if self.minutes > b.minutes:
            return True
        if self.minutes < b.minutes:
            return False
        return self.seconds > b.seconds

    def __eq__(self, b):
        return self.time == b.time and self.minutes == b.minutes and self.seconds == b.seconds

    def __str__(self):
        return self.timestamp