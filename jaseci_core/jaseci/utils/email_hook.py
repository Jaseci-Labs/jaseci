from json import dumps
import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jaseci.utils.app_state import AppState as AS
from jaseci.utils.utils import logger

################################################
#                   DEFAULTS                   #
################################################

EMAIL_CONFIG = {
    "enabled": True,
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
#                  EMAIL HOOK                   #
#################################################


class email_hook:
    app = None
    state: AS = AS.NOT_STARTED

    # ------------------- SENDER -------------------- #
    sender: str = None

    def __init__(self):
        if eh.state.is_ready() and eh.app is None:
            eh.state = AS.STARTED

            try:
                self.__emailer()
            except Exception:
                logger.exception(
                    "Skipping Emailer setup due to " "initialization failure!"
                )
                eh.app = None
                eh.state = AS.FAILED

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __emailer(self):
        configs = self.get_email_config()
        enabled = configs.get("enabled", True)
        if enabled:
            self.__convert_config(configs)
            eh.app = self.emailer_connect(configs)
            eh.state = AS.RUNNING
        else:
            eh.state = AS.DISABLED

    # ----------- BACKWARD COMPATIBILITY ------------ #
    # ---------------- TO BE REMOVED ---------------- #

    def __convert(self, holder, mapping: dict):
        for k, v in mapping.items():
            conf = self.get_glob(k)
            if not (conf is None):
                holder[v] = conf
        return holder

    def __convert_config(self, configs: dict):
        version = configs.get("version", 2)
        migrate = configs.pop("migrate", False)
        if version == 1 or migrate:
            self.__convert(
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

            configs["tls"] = (
                configs["tls"].lower() == "true"
                if type(configs["tls"]) is str
                else configs["tls"]
            )

            if migrate:
                self.save_glob("EMAIL_CONFIG", dumps(configs))

    ###################################################
    #              COMMON GETTER/SETTER               #
    ###################################################

    def emailer():
        return eh.app

    def emailer_sender(self, sender):
        eh.sender = sender

    def emailer_running(self=None):
        return eh.state == AS.RUNNING and not (eh.app is None)

    # --------------- ORM OVERRIDDEN ---------------- #

    def emailer_connect(self, configs):
        host = configs.get("host")
        port = configs.get("port")
        user = configs.get("user")
        _pass = configs.get("pass")

        eh.sender = configs.get("sender", user)

        context = ssl.create_default_context()

        if configs.get("tls", True):
            server = SMTP(host, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        else:
            server = SMTP_SSL(host, port, context=context)

        server.login(user, _pass)

        return email_config(server)

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def emailer_reset(self):
        if self.emailer_running():
            eh.app.terminate()
        eh.app = None
        eh.state = AS.NOT_STARTED
        email_hook.__init__(self)

    ####################################################
    #                      CONFIG                      #
    ####################################################

    # ORM_HOOK OVERRIDE
    def get_email_config(self):
        """Add email config"""
        return self.build_config("EMAIL_CONFIG", EMAIL_CONFIG)


eh = email_hook


# ----------------------------------------------- #


####################################################
#                   EMAIL CONFIG                   #
####################################################


class email_config:
    def __init__(self, server):
        self.server = server

    def send_custom_email(
        self,
        sender: str = None,
        recipients: list = [],
        subject: str = "Jaseci Email",
        body: tuple = ("", ""),
    ):

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = eh.sender if sender is None else sender
        message["To"] = ", ".join(recipients)

        message.attach(MIMEText(body[0], "plain"))
        message.attach(MIMEText(body[1], "html"))
        self.server.sendmail(message["From"], recipients, message.as_string())

    def terminate(self):
        self.server.quit()
