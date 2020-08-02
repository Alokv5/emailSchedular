# the first step is always the same: import all necessary components:

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from matterhook import Webhook

import pymysql


class SendEmails(object):
    def send_email(self, recipients, body):
        try:
            email_list = []
            title = body['title']
            start_time = body['start_time']
            meeting_id = body['meeting_id']
            userEmail = None
            if 'userName' in body.keys():
                userEmail = body['userName']
            else:
                userEmail = recipients

            smtp_ssl_host = 'mail.nattymail.com'  # smtp.mail.yahoo.com
            smtp_ssl_port = 587
            username = 'noreply@nattymeet.com'
            password = 'U3g5ES9UjG@2020'
            sender = 'noreply@nattymeet.com'

            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Reminder: {} @ {}'.format(title, start_time)
            msg['From'] = "noreply@nattymeet.com"
            msg['To'] = ",".join(recipients)

            html = "Hi {}," \
                   "I just wanted to send a quick reminder about our meeting on {{target.start}} . Here’s a quick map link, just in case:" \
                   "{} Let me know if anything changes. Looking forward to it!" \
                   "Thanks & Reghards" \
                   "NattyMeet & Teams".format(userEmail, start_time, meeting_id)
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            server = smtplib.SMTP('{}:{}'.format(smtp_ssl_host, smtp_ssl_port))
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.sendmail(sender, ",".join(email_list), msg.as_string())
            server.quit()
        except Exception as e:
            raise Exception("Sorry we could'nt send email for meeting_id {}".format(meeting_id))


def call_matter_hook(channel_name):
    try:
        #getdata from channel table
        mwh = Webhook('https://rnd.nattycb.com', 'x5m5u4ej6fb1mf151pqysw4fic')
        mwh.send(message='meeting reminder', channel=channel_name, username='schedule_meeting',icon_url='https://rnd.nattycb.com/static/images/favicon/favicon-32x32.png')
    except Exception as e:
        print("exception occurred while calling webhook",e)

def get_table_rows():
    try:
        db = pymysql.connect("localhost", "mattermost", "RFzWV5kdJl", "mattermost")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        query = "SELECT * FROM calendar  WHERE start_time>=now()-INTERVAL 15 MINUTE  and send_notification=0 and meeting_type='meeting'"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            body = dict()
            for row in result:
                body = {"title": row[2], "organizer": row[-1], "start_time": row[6], "meeting_id": row[1],
                        "participants": row[9]}

            participants_list = body.get("participants").split(",")
            for userEmail in participants_list:
                query = "SELECT FirstName FROM User WHERE FirstName IS NOT NULL UNION SELECT UserName AS FirstName FROM User WHERE FirstName IS NULL and Email=""\"{}\"".format(
                    userEmail)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:
                    userName = result[0]
                    body['userName'] = userName[0]
                    if row[5] is not None:
                        channel_name_list = row[5].split(",")
                        for channel_id in channel_name_list:
                            try:
                                query_channel_name = "SELECT Name FROM meetings.channels where Id = ""\"{}\"".format(channel_id.strip())
                                cursor.execute(query_channel_name)
                                res =cursor.fetchone()
                                if res is not None:
                                    call_matter_hook(res[0])
                            except Exception as e:
                                print("unable to call matter hook")
                    try:
                        SendEmails().send_email(userEmail, body)
                    except Exception as e:
                        print("error sending email")
                else:
                    try:
                        SendEmails().send_email(userEmail, body)
                    except Exception as e:
                        print("error sending email without user name")
        else:
            print("No meeting scheduled")
    except Exception as e:
        print("Error in getting data and sending email==> ", e)


while True:
    try:
        print("schedular started")
        get_table_rows()
    except Exception as e:
        print("Exception in schedular")
