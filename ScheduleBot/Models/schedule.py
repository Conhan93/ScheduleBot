import re

class ScheduleEvent:

    def __init__(self, data):
        self.time = data[0]
        self.group = data[1]
        self.lecturer = data[2]
        self.location = data[3]
        self.coursename = data[4]
        if len(data) >= 6:
            self.note = data[5]
        else:
            self.note = None
    
    def __repr__(self) -> str:
        return f'{self.time} {self.lecturer}\n{self.location} {self.coursename}'

class ScheduleDay:

    def __init__(self, event):

        result = re.findall('(.+)([0-9][0-9]\/[0-9][0-9])', event[0])[0]

        self.day = result[0]
        self.date = result[1]
        self.events = []

        self.events.append(ScheduleEvent(event[1:]))
    
    def add_event(self, data):
        self.events.append(ScheduleEvent(data))

    def __repr__(self) -> str:
        rep = f'{self.day} {self.date}\n'

        for event in self.events:
            rep += event.__repr__() + '\n'

        return rep + '\n'
    def get_group(self):
        if len(self.events) == 0:
            return None
        
        return self.events[0].group

class Schedule:

    def __init__(self, events):
        self.days = []

        for event in events:
            if(list(filter(str.isalpha, event[0][0:2]))):
                self.days.append(ScheduleDay(event))
            else:
                self.days[-1].add_event(event)
        
        self.group = self.days[0].get_group()

    def __repr__(self) -> str:
        rep = f'{self.group}\n\n'

        for day in self.days:
            rep += day.__repr__()
        
        return rep
