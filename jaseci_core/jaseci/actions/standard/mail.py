from jaseci.actions.live_actions import jaseci_action
from jaseci.mail.mail import email_config as ec


@jaseci_action()
def send(sender, recipients, subject, text, html, meta):
    with ec(meta["h"]) as mailer:
        mailer.send_custom_email(sender, recipients, subject, (text, html))
