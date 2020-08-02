# the first step is always the same: import all necessary components:

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
                    SendEmails().send_email(userEmail, body)
                else:
                    SendEmails().send_email(userEmail, body)
    except Exception as e:
        print("Error in getting data and sending email==> ", e)


while True:
    try:
        print("schedular started")
        get_table_rows()
    except Exception as e:
        print("Exception in schedular")
