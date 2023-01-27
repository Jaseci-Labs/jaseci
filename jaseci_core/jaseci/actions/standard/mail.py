from jaseci.actions.live_actions import jaseci_action
from jaseci.svc import MetaService


@jaseci_action()
def send(sender, recipients, subject, text, html):
    MetaService().get_service("mail").poke().send_custom_email(
        sender, recipients, subject, (text, html)
    )
