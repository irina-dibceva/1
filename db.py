import datetime
import logging

import psycopg2

today = datetime.date.today()
from find_work.secret import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER

try:
    conn = psycopg2.connect(dbname='DB_NAME', user='DB_USER', host='DB_HOST', password='DB_PASSWORD')
except:
    logging.exception('Unable to open DB - {}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, speciality_id FROM subscribers_subscriber WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    print(cities_qs)

    conn.commit()
    cur.close()
    conn.close()
