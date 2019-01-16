import json
from dateutil import rrule
from datetime import datetime, timedelta
from random import randint

'''
72 konferencje
72 nazwy konferencji
daty - równy podział trzech lat na 72
czas trwania - 36 2-dniowych i 36 3-dniowych
cost = rand(100, 1000)


'''
class Conference:
    def __init__(self, name):
        self.name = name + ' Conference'

if __name__ == "__main__":
    #Conferences
    with open('conf_names', 'r') as infile:
        conference_names = infile.read().split('\n')

    date_zero = datetime(2019, 1, 1)
    date_max = datetime(2021, 12, 31)
    dates_start = list(rrule.rrule(rrule.WEEKLY, dtstart=date_zero, until=date_max, interval=2))

    print(len(dates_start), len(conference_names))
    for i in range(len(dates_start)):
        conf_id = i
        conf_name = conference_names[i]
        date_begin = dates_start[i] + timedelta(days=randint(-1, 1)) + timedelta(hours=randint(8, 10))
        date_end = date_begin + timedelta(days=randint(1,2)) + timedelta(hours=randint(8, 10))
        cost = randint(10, 100)*10
        max_participants = randint(10, 30)*10
        studentDiscount = round(randint(5, 8)*0.1, 1)
        print(conf_id, conf_name, date_begin, date_end, cost, max_participants, studentDiscount, sep=';')