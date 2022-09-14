from jaseci.actions.live_actions import jaseci_action
from jaseci.svc.mail.mail_svc import mail_svc
from jaseci.svc.common_svc import MAIL_ERR_MSG
from jaseci.utils.utils import logger


@jaseci_action()
def send(sender, recipients, subject, text, html, meta):
    ma = mail_svc()
    if ma.is_running():
        ma.app.send_custom_email(sender, recipients, subject, (text, html))
    else:
        logger.error(MAIL_ERR_MSG)
