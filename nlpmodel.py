"""
THIS PROGRAM CONTAINS NATURAL LANGUAGE MODEL
"""
import datetime as dt
from datetime import date
from datetime import timedelta as td
import spacy
from spacy.pipeline import EntityRuler
nlp = spacy.load("en_core_web_sm")

def initialize():
    # create NLP engine
    nlp = spacy.load("en_core_web_sm")
    # define rules for language analytics
    ruler1 = EntityRuler(nlp)
    pattern1 = [{"label": "FLEET", "pattern": "Fleets"}, {"label": "FLEET", "pattern": "Fleet"},
                {"label": "FLEET", "pattern": "Trucks"}, {"label": "FLEET", "pattern": "Truck"},
                {"label": "FLEET", "pattern": "Rails"}, {"label": "FLEET", "pattern": "Rail"},
                {"label": "FLEET", "pattern": "Ships"}, {"label": "FLEET", "pattern": "Ship"},
                {"label": "FLEET", "pattern": "Cargos"}, {"label": "FLEET", "pattern": "Cargo"},
                {"label": "FLEET_STATUS", "pattern": "Planned"}, {"label": "FLEET_STATUS", "pattern": "Active"},
                {"label": "FLEET_STATUS", "pattern": "Running"}, {"label": "FLEET_STATUS", "pattern": "Inactive"},
                {"label": "FLEET_STATUS", "pattern": "Closed"}, {"label": "FLEET_STATUS", "pattern": "Hold"},
                {"label": "TRACK", "pattern": "Tracks"}, {"label": "TRACK", "pattern": "Track"},
                {"label": "TRACK_STATUS", "pattern": "Operate"}, {"label": "TRACK_STATUS", "pattern": "Delayed"},
                {"label": "TRACK_STATUS", "pattern": "Arrived"}, {"label": "TRACK_STATUS", "pattern": "Started"},
                {"label": "TRACK_STATUS", "pattern": "Broken"}, {"label": "TRACK_STATUS", "pattern": "Transit"},
                {"label": "TRACK_STATUS", "pattern": "Reached"}, {"label": "TRACK_STATUS", "pattern": "Completed"},
                {"label": "DAY_STATUS", "pattern": "Today"}, {"label": "DAY_STATUS", "pattern": "today"},
                {"label": "DAY_STATUS", "pattern": "Yesterday"}, {"label": "DAY_STATUS", "pattern": "yesterday"},
                {"label": "DAY_STATUS", "pattern": "Tomorrow"}, {"label": "DAY_STATUS", "pattern": "tomorrow"},
                {"label": "TOTAL", "pattern": "Total"}, {"label": "TOTAL", "pattern": "total"}
             ]
    # add the rules to NLP engie
    ruler1.add_patterns(pattern1)
    nlp.add_pipe(ruler1, before='ner')
    return nlp
# this function is called from flask web service to convert user question into sql
def convert_text_sql(s):
    nlp = initialize()
    s =s.title()
    doc = nlp(s)
    query = u''
    LIST_FLEETS = ['truck', 'trucks', 'rail', 'rails', 'ship', 'ships', 'cargo', 'cargos']
    LIST_TRACKS_STATUS = ['planned', 'started', 'broken', 'transit', 'reached', 'completed','delayed']

    for ent in doc.ents:
        exp = ent.text
        print(ent.text, ent.label_)
        exp = exp.lower()
        if ent.label_ == "DAY_STATUS":
            now = date.today()
            for e in doc.ents:
                if e.label_ == "TRACK_STATUS":
                    ex = e.text
                    if exp == 'today':
                        query = 'select * from TRACK where operation_status = ' + '\'' + ex.title() + '\'' + 'and eta = ' + '\'' + str(now) + '\''
                    elif exp == 'yesterday':
                        d = now - td(days = 1)
                        query = 'select * from TRACK where operations_status = ' + '\'' + ex.title() + '\'' + 'and eta = ' + '\'' + str(d) + '\''
                    elif exp == 'tomorrow':
                        d = now + td(days=1)
                        query = 'select * from TRACK where operation_status = ' + '\'' + ex.title() + '\'' + 'and eta = ' + '\''+ str(d)+ '\''
                    else:
                        m = now.month
                        query = 'select * from TRACK where operation_status = ' + '\'' + ex.title() + '\''
                if len(query) > 1:
                    return query
        if ent.label_ == "TOTAL":
            for e in doc.ents:
                if e.label_ == "TRACK":
                    query = 'select convert(count(*), char(10)) as total from TRACK'
                    return query
                elif e.label_ == "TRACK_STATUS":
                    ex = e.text
                    if exp in LIST_TRACKS_STATUS:
                        query = 'select convert(count(*), char(10)) as total from TRACK where operation_status = ' + '\'' + ex.title() + '\''
                        return query
                elif e.label_ == "FLEET":
                    query = 'select convert(count(*), char(10)) as total from FLEET'
                    return query
                elif e.label_ == "FLEET_STATUS":
                    ex = e.text
                    query = 'select convert(count(*), char(10)) as total from FLEET where status = ' + '\'' + ex.title() + '\''
                    return query
        if ent.label_ == "TRACK_STATUS":
            if exp in LIST_TRACKS_STATUS:
                query = 'select * from TRACK where operation_status = ' + '\'' + exp.title() + '\''
                return query
        elif ent.label_ == "TRACK":
            query = 'select * from TRACK'
            return query
        elif ent.label_ == "FLEET_STATUS":
            query = 'select * from FLEET where status = ' + '\'' + exp.title() + '\''
            return query
        elif ent.label_ == "FLEET":
            if exp in LIST_FLEETS:
                query = 'select * from FLEET where fleet_type = ' + '\''+ exp.title() + '\''
                return query
            else:
                query = 'select * from FLEET'
                return query

    return None

#USE THIS BLOCK OF CODE FOR UNIT TESTING OR DEBUGGING
# def test():
#     initialize()
#     s = u'list of in transit tracks'
#     #s = u'completed tracks'
#     #s=x.title()
#     print (s)
#     doc=nlp(s)
#     for ent in doc.ents:
#         print(ent.text, ent.label_)
#     sql = convert_text_sql(s)
#     if sql != None:
#         print(sql)
#     else:
#         print('Sorry... unknown query!!!')
#
#
# test()
