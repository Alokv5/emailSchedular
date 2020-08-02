# the first step is always the same: import all necessary components:

import pymysql

from email_sender.MailSenderUtility import SendEmails


def get_table_rows():
    try:
        db = pymysql.connect("localhost", "root", "alok@1990", "meetings")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        query = "SELECT * FROM calendar  WHERE start_time>=now()-INTERVAL 150 MINUTE  and send_notification=0 and meeting_type='meeting'"
        cursor.execute(query)
        result = cursor.fetchall()
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
