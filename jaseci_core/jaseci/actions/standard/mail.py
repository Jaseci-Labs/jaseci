from jaseci.actions.live_actions import jaseci_action
from jaseci.svcs.mail.mail_svc import mail_svc
from jaseci.utils.utils import logger

MAIL_ERR_MSG = "Mail service is disabled or not yet configured!"


@jaseci_action()
def send(sender, recipients, subject, text, html, meta):
    ma = mail_svc()
    if ma.is_running():
        ma.app.send_custom_email(sender, recipients, subject, (text, html))
    else:
        logger.error(MAIL_ERR_MSG)
