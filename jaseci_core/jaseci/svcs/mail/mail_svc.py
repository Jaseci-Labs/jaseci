from json import dumps
import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jaseci.svcs import common_svc, ServiceState as SS
from jaseci.utils.utils import logger

################################################
#                   DEFAULTS                   #
################################################

EMAIL_CONFIG = {
    "enabled": True,
    "quiet": True,
    "version": 2,
    "tls": True,
    "host": "smtp.gmail.com",
    "port": 587,
    "sender": "Jaseci Admin<boyong@jaseci.org>",
    "user": "jaseci.dev@gmail.com",
    "pass": "yrtviyrdzmzdpjxg",
    "backend": "smtp",
    "templates": {
        "activation_subj": "Please activate your account!",
        "activation_body": "Thank you for creating an account!\n\n"
        "Activation Code: {{code}}\n"
        "Please click below to activate:\n{{link}}",
        "activation_html_body": "Thank you for creating an account!<br><br>"
        "Activation Code: {{code}}<br>"
        "Please click below to activate:<br>"
        "{{link}}",
        "resetpass_subj": "Password Reset for Jaseci Account",
        "resetpass_body": "Your Jaseci password reset token is: {{token}}",
        "resetpass_html_body": "Your Jaseci password reset" "token is: {{token}}",
    },
}

#################################################
#                  EMAIL APP                   #
#################################################


class mail_svc(common_svc):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        super().__init__(mail_svc)

        try:
            if self.is_ready():
                self.state = SS.STARTED
                self.__mail(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    "Skipping Mail setup due to initialization failure!\n"
                    f"{e.__class__.__name__}: {e}"
                )
            self.app = None
            self.state = SS.FAILED

    def __mail(self, hook):
        configs = self.get_config(hook)
        enabled = configs.get("enabled", True)

        if enabled:
            self.quiet = configs.pop("quiet", False)
            self.__convert_config(hook, configs)
            self.app = self.connect(configs)
            self.state = SS.RUNNING
        else:
            self.state = SS.DISABLED

    # ----------- BACKWARD COMPATIBILITY ------------ #
    # ---------------- TO BE REMOVED ---------------- #

    def __convert(self, hook, holder, mapping: dict):
        for k, v in mapping.items():
            if hook.has_glob(k):
                conf = hook.get_glob(k)
                if not (conf is None):
                    if v == "tls":
                        holder[v] = conf.lower() == "true"
                    else:
                        holder[v] = conf
        return holder

    def __convert_config(self, hook, configs: dict):
        version = configs.get("version", 2)
        migrate = configs.pop("migrate", False)
        if version == 1 or migrate:
            self.__convert(
                hook,
                configs,
                {
                    "EMAIL_BACKEND": "backend",
                    "EMAIL_HOST": "host",
                    "EMAIL_PORT": "port",
                    "EMAIL_HOST_USER": "user",
                    "EMAIL_HOST_PASSWORD": "pass",
                    "EMAIL_DEFAULT_FROM": "sender",
                    "EMAIL_USE_TLS": "tls",
                },
            )

            if "templates" not in configs:
                configs["templates"] = {}

            self.__convert(
                hook,
                configs["templates"],
                {
                    "EMAIL_ACTIVATION_SUBJ": "activation_subj",
                    "EMAIL_ACTIVATION_BODY": "activation_body",
                    "EMAIL_ACTIVATION_HTML_BODY": "activation_html_body",
                    "EMAIL_RESETPASS_SUBJ": "resetpass_subj",
                    "EMAIL_RESETPASS_BODY": "resetpass_body",
                    "EMAIL_RESETPASS_HTML_BODY": "resetpass_html_body",
                },
            )

            if migrate:
                hook.save_glob("EMAIL_CONFIG", dumps(configs))

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook):
        if self.is_running():
            self.app.terminate()
        self.build(hook)

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def connect(self, configs):
        host = configs.get("host")
        port = configs.get("port")
        user = configs.get("user")
        _pass = configs.get("pass")
        sender = configs.get("sender", user)

        context = ssl.create_default_context()

        if configs.get("tls", True):
            server = SMTP(host, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        else:
            server = SMTP_SSL(host, port, context=context)

        server.login(user, _pass)

        return emailer(server, sender)

    def get_config(self, hook) -> dict:
        return hook.build_config("EMAIL_CONFIG", EMAIL_CONFIG)


# ----------------------------------------------- #


####################################################
#                   EMAIL CONFIG                   #
####################################################


class emailer:
    def __init__(self, server, sender):
        self.server = server
        self.sender = sender

    def send_custom_email(
        self,
        sender: str = None,
        recipients: list = [],
        subject: str = "Jaseci Email",
        body: tuple = ("", ""),
    ):

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self.sender if sender is None else sender
        message["To"] = ", ".join(recipients)

        message.attach(MIMEText(body[0], "plain"))
        message.attach(MIMEText(body[1], "html"))
        self.server.sendmail(message["From"], recipients, message.as_string())

    def terminate(self):
        self.server.quit()
