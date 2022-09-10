from jaseci.actions.live_actions import jaseci_action
from jaseci.svcs.mail.mail_svc import mail_svc


@jaseci_action()
def send(sender, recipients, subject, text, html):
    ma = mail_svc()
    if ma.is_running():
        ma.app.send_custom_email(sender, recipients, subject, (text, html))
