import re

class ScheduleEvent:
    """
    Class that holds information about an event or
    a schedule row on TimeEdit.
    """

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
    
    def __str__(self) -> str:
        if self.note:
            return f'{self.time} {self.lecturer}\n{self.location} {self.coursename}\n{self.note}'
        else:
            return f'{self.time} {self.lecturer}\n{self.location} {self.coursename}'

class ScheduleDay:
    """
    Class that contains all the scheduled events of a particular day.
    """

    def __init__(self, event):

        result = re.findall('([a-öA-Ö]{3,4})([0-9]{1,2}\/[0-9]{1,2})', event[0])[0]

        self.day = result[0]
        self.date = result[1]
        self.events = []

        self.events.append(ScheduleEvent(event[1:]))
    
    def add_event(self, data):
        self.events.append(ScheduleEvent(data))

    def __str__(self) -> str:
        rep = f'{self.day} {self.date}\n'

        for event in self.events:
            rep += str(event) + '\n'

        return rep + '\n'
    def get_group(self):
        if len(self.events) == 0:
            return None
        
        return self.events[0].group

class Schedule:
    """
    Class that holds a schedule, constructs a schedule from
    a list of schedule entries created by PageParser.
    """
    def __init__(self, events):
        self.days = []

        for event in events:
            #if event starts with day, create new day from event
            if str.isalpha(event[0][0:2]):
                self.days.append(ScheduleDay(event))
            
            # else add event to previous day
            else:
                self.days[-1].add_event(event)
        
        self.group = self.days[0].get_group()

    def __str__(self) -> str:
        rep = f'{self.group}\n\n'

        for day in self.days:
            rep += str(day)
        
        return rep
    
    def __len__(self) -> int:
        return len(self.days)
