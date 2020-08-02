from matterhook import Webhook

# mandatory parameters are url and your webhook API key
def call_matter_hook():
    try:
        mwh = Webhook('https://rnd.nattycb.com', 'x5m5u4ej6fb1mf151pqysw4fic')
        mwh.send(message='meeting reminder', channel='town-square', username='schedule_meeting',icon_url='https://rnd.nattycb.com/static/images/favicon/favicon-32x32.png')
    except Exception as e:
        print("exception occured",e)



call_matter_hook()