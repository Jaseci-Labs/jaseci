import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from json import dumps
from smtplib import SMTP, SMTP_SSL

from jaseci.svc import CommonService
from .config import MAIL_CONFIG


#################################################
#                  EMAIL APP                   #
#################################################


class MailService(CommonService):

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self, hook=None):
        self.__convert_config(hook)
        self.app = self.connect()

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

    def __convert_config(self, hook):
        version = self.config.get("version", 2)
        migrate = self.config.get("migrate", False)
        if version == 1 or migrate:
            self.__convert(
                hook,
                self.config,
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

            if "templates" not in self.config:
                self.config["templates"] = {}

            self.__convert(
                hook,
                self.config["templates"],
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
                self.config["migrate"] = False
                hook.save_glob("MAIL_CONFIG", dumps(self.config))

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def reset(self, hook):
        if self.is_running():
            self.app.terminate()

        super().reset(hook)

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def connect(self):
        host = self.config.get("host")
        port = self.config.get("port")
        user = self.config.get("user")
        _pass = self.config.get("pass")
        sender = self.config.get("sender", user)

        context = ssl.create_default_context()

        if self.config.get("tls", True):
            server = SMTP(host, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        else:
            server = SMTP_SSL(host, port, context=context)

        server.login(user, _pass)

        return Mailer(server, sender)

    def build_config(self, hook) -> dict:
        return hook.service_glob("MAIL_CONFIG", MAIL_CONFIG)


# ----------------------------------------------- #


####################################################
#                   EMAIL CONFIG                   #
####################################################


class Mailer:
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
