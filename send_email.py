import psycopg2
import logging
import datetime
import os
import requests
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today = datetime.date.today()
ten_days_ago = datetime.date.today() - datetime.timedelta(10)

dir = os.path.dirname(os.path.abspath('db.py'))
path = ''.join([dir, '\\find_work\\secret.py'])
if os.path.exists(path):
    from find_work.secret import (DB_PASSWORD, DB_HOST, DB_NAME, DB_USER,
                                MAILGUN_KEY, API, MAIL_SERVER,
                                PASSWORD_AWARD, USER_AWARD, FROM_EMAIL)
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    api_key = os.environ['MJ_KEY']  # KEY_PUBLIC
    api_secret = os.environ['MJ_SECRET']  # KEY_PRIVATE
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    PASSWORD_AWARD = os.environ.get('PASSWORD_AWARD')
    USER_AWARD = os.environ.get('USER_AWARD')
    FROM_EMAIL = os.environ.get('FROM_EMAIL')

FROM_ = '{email}'.format(email=FROM_EMAIL)
SUBJECT = 'List of vacancies for {}'.format(today)
template = '''<!doctype html><html lang="en">
                <head><meta charset="utf-8"></head>
                <body>'''
end = '</body></html>'
text = '''Список вакансий, согласно Ваших предпочтений с сервиса JobFinder'''

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, speciality_id FROM subscribers_subscriber 
                    WHERE is_active=%s;""", (True,))
    cities_qs = list(set(cur.fetchall()))
    # print(cities_qs)

    for pair in cities_qs:
        content = '''<h3>List of vacancies for you. </h3>
                    <hr><br/><br/>'''
        city = pair[0]
        speciality = pair[1]
        cur.execute(""" SELECT email FROM subscribers_subscriber 
                            WHERE is_active=%s 
                            AND city_id=%s AND speciality_id=%s;""",
                    (True, city, speciality))
        email_qs = cur.fetchall()
        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url_vacancy, title, description, company 
                        FROM scraping_vacancy WHERE city_id=%s 
                        AND speciality_id=%s AND timestamp=%s; """,
                    (city, speciality, today))
        jobs_qs = cur.fetchall()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'List of vacancy for  {}'.format(today)
        # msg['From'] = 'Вакансии <{email}>'.format(email=FROM_EMAIL)
        msg['From'] = FROM_
        mail = smtplib.SMTP()
        mail.connect(MAIL_SERVER, 25)
        mail.ehlo()
        mail.starttls()
        mail.login(USER_AWARD, PASSWORD_AWARD)
        if jobs_qs:
            for job in jobs_qs:
                content += '<a href="{}" target="_blank">'.format(job[0])
                content += '{}</a><br/>'.format(job[1])
                content += '<p>{}</p>'.format(job[2])
                content += '<p>{}</p><br/>'.format(job[3])
                content += '<hr/><br/><br/>'
            content += '''<h4>You send this mail because you is subscriber of <a href="{}" target="_blank">
                            <h4><br/>
                            <h5>Thanks for you with me! </h5><br/>
                            '''.format('https://jobfinderapp.herokuapp.com/')
            html_m = template + content + end
            part = MIMEText(html_m, 'html')
            msg.attach(part)
            mail.sendmail(FROM_EMAIL, emails, msg.as_string())

        else:
            content = '''<h3>На сегодня, список вакансий по 
                                Вашему запросу, пуст.</h3> '''
            content += '''<h4>You send this mail because you is subscriber of <a href="{}" target="_blank">
                            <h4><br/>
                            <h5>Thanks for you with me! </h5><br/>
                            '''.format('https://jobfinderapp.herokuapp.com/')
            html_m = template + content + end
            part = MIMEText(html_m, 'html')
            msg.attach(part)
            mail.sendmail(FROM_EMAIL, emails, msg.as_string())

        mail.quit()
    conn.commit()
    cur.close()
    conn.close()


def send_simple_message():
    return requests.post("https://api.mailgun.net/v3/sandbox416a538053f040199cd9bcedcf5ce10d.mailgun.org/messages",
                         auth=("api", "54dfca2a8a0899f39e071a671449044c-9949a98f-552437e3"),
                         data={
                             "from": "Mailgun Sandbox <postmaster@sandbox416a538053f040199cd9bcedcf5ce10d.mailgun.org>",
                             "to": "Python <irinadibceva@gmail.com>",
                             "subject": "Hello Python",
                             "text": "Congratulations Python, you just sent an email with Mailgun!  You are truly "
                                     "awesome!"})
