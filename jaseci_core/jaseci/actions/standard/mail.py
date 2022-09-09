from jaseci.actions.live_actions import jaseci_action
from jaseci.app.mail.mail_app import mail_app


@jaseci_action()
def send(sender, recipients, subject, text, html):
    ma = mail_app()
    if ma.is_running():
        ma.app.send_custom_email(sender, recipients, subject, (text, html))
