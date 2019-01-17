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

    def __str__(self):
        return '( ' + str(self.id) + ', ' + str(self.conf_id) + ', CAST(\'' + str(self.day) + '\' AS date),'

class Workshop:
    def __init__(self, id, workshop_id, confday_id, date_b, date_e, cost):
        self.id = id
        self.workshop_id = workshop_id
        self.confday_id = confday_id
        self.date_begin = date_b
        self.date_end = date_e
        self.cost = cost

    def __str__(self):
        return '(' + str(self.id) + ', ' + str(self.workshop_id) + ', ' + str(self.confday_id) + ', ' + 'CAST(\'' + str(self.date_begin) + '\' AS smalldatetime), CAST(\'' + str(self.date_end) + '\' AS smalldatetime), ' + str(self.cost) + '),'

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

def generate_conf_days(id, conf):
    conf_days = []
    days = abs((conf.date_begin - conf.date_end).days)
    for d in range(days):
        conf_days.append(ConferenceDay(id, conf.id, (conf.date_begin + timedelta(days=d)).date()))
        id += 1
    return conf_days, id

def generate_workshop(id, conf, conf_day):
    workshops = []
    for i in range(4):
        workshop_info_id = conf.id//4 + i
        date_begin = conf_day.day + timedelta(hours=10 + i)
        date_end = date_begin + timedelta(days=1)
        cost = randint(2, 4)*50
        workshops.append(Workshop(id, workshop_info_id, conf_day.id, date_begin, date_end, cost))
        id += 1
    return workshops, id

def generate():
    confs = generate_conferences()
    with open('fill_conferences.sql', 'w') as out_confs:
        out_confs.write('INSERT INTO Conferences (id, Address_id, name, date_begin, date_end, cost, maximumParticipants, studentDiscount)\nVALUES\n')
        with open('fill_discounts.sql', 'w') as out_discounts:
            out_discounts.write('INSERT INTO CostDiscount (id, Conference_id, discount, date_begin, date_end)\nVALUES\n')
            with open('fill_days.sql', 'w') as out_days:
                out_days.write('INSERT INTO ConferenceDay (id, Conferences_id, day)\nVALUES\n')
                with open('fill_workshops.sql', 'w') as out_workshops:
                    out_workshops.write('INSERT INTO Workshop (id, Workshopinformation_id, ConferenceDay_id, date_begin, date_end, cost)\nVALUES\n')
                    disc_id = 0
                    days_id = 0
                    workshop_id = 0
                    for c in confs:
                        discounts, disc_id = generate_discounts(disc_id, c)
                        days, days_id = generate_conf_days(days_id, c)
                        out_confs.write(str(c) + '\n')
                        for d in discounts:
                            out_discounts.write(str(d) + '\n')
                        for d in days:
                            out_days.write(str(d) + '\n')
                            workshops, workshop_id = generate_workshop(workshop_id, c, d)
                            for w in workshops:
                                out_workshops.write(str(w)+ '\n')

if __name__ == "__main__":
    # with open('fill_student.sql', 'w') as out_student:
    #     out_student.write('INSERT INTO Student (id, cardNumber)\nVALUES\n')
    #     for i in range(0, 1000, 3):
    #         out_student.write('( ' + str(i) + ', ' + str(randint(100000, 999999)) + '),\n')
    # with open('fill_individual.sql', 'w') as out_ind:
    #     out_ind.write('INSERT INTO InfividualParticipant (id, additionalinformation)\nVALUES\n')
    #     for i in range(1, 1000, 3):
    #         out_ind.write('( ' + str(i) + ', \'Lorem ipsum dolor sit amet.\'),\n')
    with open('fill_cmp.sql', 'w') as out_cmp:
        out_cmp.write('INSERT INTO CompanyParticipant (id, Company_id)\nVALUES\n')
        for i in range(2, 1000, 3):
            out_cmp.write('( ' + str(i) + ', ' + str(randint(1, 100)) + '),\n')