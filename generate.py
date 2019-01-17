import json
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from random import randint


class Conference:
    def __init__(self, id, name, date_begin, date_end, cost, max_participants, student_discount):
        self.id = id
        self.name = name + ' Conference'
        self.date_begin = date_begin
        self.date_end = date_end
        self.cost = cost
        self.max_participants = max_participants
        self.student_discount = student_discount

    def __str__(self):
        return '(' + str(self.id) + ', ' + '\'' + self.name + '\', ' + 'CAST(\'' + str(self.date_begin) + '\' AS smalldatetime), CAST(\'' + str(self.date_end) + '\' AS smalldatetime), ' + str(self.cost) + ', ' + str(self.max_participants) + ', ' + str(self.student_discount) + '),'

class Discount:
    def __init__(self, conf_id, discount, date_begin, date_end):
        self.conf_id = conf_id
        self.discount = discount
        self.date_begin = date_begin
        self.date_end = date_end

class workshop_info:
    def __init__(self, id, name, max_parts):
        self.id = id
        self.name = name
        self.desc = 'Lorem ipsum dolor sit amet.'
        self.max_pars = max_parts

    def __str__(self):
        return '(' + str(self.id) + ', \'' + self.name + '\', \'' + self.desc + '\', ' + str(self.max_pars) + '),'

class ConferenceDay:
    def __init__(self, id, conf_id, day):
        self.id = id
        self.conf_id = conf_id
        self.day = day



def generate_conferences():
    conferences = []
    with open('conf_names', 'r') as infile:
        conference_names = infile.read().split('\n')

    date_zero = datetime(2019, 1, 1)
    date_max = datetime(2021, 12, 31)
    dates_start = list(rrule.rrule(rrule.WEEKLY, dtstart=date_zero, until=date_max, interval=2))

    for i in range(len(dates_start)):
        conf_id = i
        conf_name = conference_names[i]
        date_begin = dates_start[i] + timedelta(days=randint(-1, 1)) + timedelta(hours=randint(8, 10))
        date_end = date_begin + timedelta(days=randint(1,2)) + timedelta(hours=randint(8, 10))
        cost = randint(10, 100)*10
        max_participants = randint(10, 30)*10
        studentDiscount = round(randint(5, 8)*0.1, 1)
        conferences.append(Conference(conf_id, conf_name, date_begin, date_end, cost, max_participants, studentDiscount))
    return conferences

def generate_discounts(conference):
    discounts = []
    months_before = randint(3, 6)
    discount_jump = round(randint(5, 10)*.01, 2)
    cr_discount = 1
    cr_date_end = conference.date_begin
    for i in range(months_before):
        conf_id = conference.id
        discount = cr_discount
        cr_discount -= discount_jump
        date_end = cr_date_end
        cr_date_end -= timedelta(days=30)
        date_begin = cr_date_end
        discounts.append(Discount(conf_id, round(discount, 2), date_begin, date_end))
    return discounts

def generate_workshop_info(id, conf_name):
    workshops = []
    for i in range(4):
        if i == 0:
            name = conf_name.replace('Conference', 'Entry-level')
        elif i == 1:
            name = conf_name.replace('Conference', 'Beginner')
        elif i == 2:
            name = conf_name.replace('Conference', 'Advanced')
        elif i == 3:
            name = conf_name.replace('Conference', 'Master')
        max_parts = randint(2, 4) * 5
        workshops.append(workshop_info(id + i, name, max_parts))
    return workshops




if __name__ == "__main__":
    #Conferences
    confs = generate_conferences()
    # with open('fill_workshopinfo.sql', 'a') as outfile:
    #     i = 0
    #     for conf in confs:
    #         workshops = generate_workshop_info(i, conf.name)
    #         for w in workshops:
    #             outfile.write(str(w) + '\n')
    #         i += 4
    streets = '''2559 West Place
74 Valley Edge Road
39 Knutson Road
02 Crownhardt Lane
999 Blaine Alley
53412 Londonderry Park
0505 Esch Alley
8782 Springview Pass
725 Dwight Place
1 Sutherland Court
98898 Center Pass
0535 Shopko Avenue
37723 Grasskamp Circle
356 Donald Point
9 Cherokee Avenue
4 Forest Alley
706 Helena Pass
64 Arapahoe Pass
6406 Reinke Terrace
8 Debs Alley
662 Delaware Junction
427 Roth Terrace
0 Daystar Point
43 Westridge Junction
55 Hermina Junction
3 Holy Cross Plaza
39 Vidon Lane
42155 School Street
6 Farwell Road
0 Talmadge Way
3 Melby Parkway
25 Bellgrove Center
1 Hoffman Drive
5 Messerschmidt Crossing
9 Esker Avenue
8 Nevada Park
20 Oneill Hill
1 Spohn Center
639 Daystar Terrace
3 Independence Terrace'''
    i = 0
    for street in streets.split('\n'):
        print('(' + str(i) + ', ' + str(randint(0, 29)) + ', \'' + street + '\'),')
        i += 1

