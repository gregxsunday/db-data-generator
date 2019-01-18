insert_query = 'INSERT INTO ConferenceParticipant (id, ConferenceReservation_id) VALUES '
fp = 'fill_confParticipants.sql'
with open(fp, 'r') as f:
    lines = f.read()
with open(fp[:-3]+'2.sql', 'w') as f:
    for l in lines.split('\n'):
        f.write(insert_query + l[:-1] + ';\n')