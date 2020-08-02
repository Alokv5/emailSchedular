#!/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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


'''while True:
    SendEmails().conncetsql()'''
