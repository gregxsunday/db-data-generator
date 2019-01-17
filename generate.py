import json
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from random import randint


class Conference:
    def __init__(self, id, addr_id, name, date_begin, date_end, cost, max_participants, student_discount):
        self.id = id
        self.addr_id = addr_id
        self.name = name + ' Conference'
        self.date_begin = date_begin
        self.date_end = date_end
        self.cost = cost
        self.max_participants = max_participants
        self.student_discount = student_discount

    def __str__(self):
        return '(' + str(self.id) + ', ' + str(self.addr_id) + ', \'' + self.name + '\', ' + 'CAST(\'' + str(self.date_begin) + '\' AS smalldatetime), CAST(\'' + str(self.date_end) + '\' AS smalldatetime), ' + str(self.cost) + ', ' + str(self.max_participants) + ', ' + str(self.student_discount) + '),'

class Discount:
    def __init__(self, id, conf_id, discount, date_begin, date_end):
        self.id = id
        self.conf_id = conf_id
        self.discount = discount
        self.date_begin = date_begin
        self.date_end = date_end

    def __str__(self):
        return '( ' + str(self.id) + ', ' + str(self.conf_id) + ', ' + str(self.discount) + ', CAST(\'' + str(self.date_begin) + '\' AS smalldatetime), CAST(\'' + str(self.date_end) + '\' AS smalldatetime)),'

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
        addr_id = randint(0, 39)
        conferences.append(Conference(conf_id, addr_id, conf_name, date_begin, date_end, cost, max_participants, studentDiscount))
    return conferences

def generate_discounts(id, conference):
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
        discounts.append(Discount(id, conf_id, round(discount, 2), date_begin, date_end))
        id += 1
    return discounts, id

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
    with open('fill_conferences.sql', 'w') as outfile:
        disc_id = 0
        for c in confs:
            discounts, disc_id = generate_discounts(disc_id, c)
            outfile.write(str(c) + '\n')
            with open('fill_discounts.sql', 'a') as out_discounts:
                for d in discounts:
                    out_discounts.write(str(d) + '\n')
    # with open('fill_workshopinfo.sql', 'a') as outfile:
    #     i = 0
    #     for conf in confs:
    #         workshops = generate_workshop_info(i, conf.name)
    #         for w in workshops:
    #             outfile.write(str(w) + '\n')
    #         i += 4

