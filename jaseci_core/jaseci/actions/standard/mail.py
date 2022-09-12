from jaseci.actions.live_actions import jaseci_action
from jaseci.svcs.mail.mail_svc import mail_svc
from jaseci.svcs.common_svc import MAIL_ERR_MSG


@jaseci_action()
def send(sender, recipients, subject, text, html, meta):
    ma = mail_svc()
    if ma.is_running():
        ma.app.send_custom_email(sender, recipients, subject, (text, html))
    else:
        meta["interp"].rt_error(MAIL_ERR_MSG)
