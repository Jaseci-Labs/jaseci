import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from json import dumps
from smtplib import SMTP, SMTP_SSL

from jaseci.svc import CommonService, ServiceState as Ss
from jaseci.utils.utils import logger
from .common import MAIL_CONFIG


#################################################
#                  EMAIL APP                   #
#################################################


class MailService(CommonService):

    ###################################################
    #                   INITIALIZER                   #
    ###################################################

    def __init__(self, hook=None):
        super().__init__(MailService)

        try:
            if self.is_ready():
                self.state = Ss.STARTED
                self.__mail(hook)
        except Exception as e:
            if not (self.quiet):
                logger.error(
                    "Skipping Mail setup due to initialization failure!\n"
                    f"{e.__class__.__name__}: {e}"
                )
            self.app = None
            self.state = Ss.FAILED

    def __mail(self, hook):
        configs = self.get_config(hook)
        enabled = configs.get("enabled", True)

        if enabled:
            self.quiet = configs.pop("quiet", False)
            self.__convert_config(hook, configs)
            self.app = self.connect(configs)
            self.state = Ss.RUNNING
        else:
            self.state = Ss.DISABLED

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
                hook.save_glob("MAIL_CONFIG", dumps(configs))

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

        return Mailer(server, sender)

    def get_config(self, hook) -> dict:
        return hook.build_config("MAIL_CONFIG", MAIL_CONFIG)


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
