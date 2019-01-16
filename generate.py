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

class Discount:
    def __init__(self, conf_id, discount, date_begin, date_end):
        self.conf_id = conf_id
        self.discount = discount
        self.date_begin = date_begin
        self.date_end = date_end

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

if __name__ == "__main__":
    #Conferences
    confs = generate_conferences()
    
