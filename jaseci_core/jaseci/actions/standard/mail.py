from jaseci.actions.live_actions import jaseci_action
from jaseci import JsOrc
from jaseci.svc.mail_svc import Mailer


@jaseci_action()
def send(sender, recipients, subject, text, html):
    JsOrc.svc("mail").poke(Mailer).send_custom_email(
        sender, recipients, subject, (text, html)
    )
