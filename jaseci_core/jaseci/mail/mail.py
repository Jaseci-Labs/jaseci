"""
This module includes code related to configuring Jaseci's mail serving
"""
import ssl
from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_defaults = {
    "EMAIL_USE_TLS": "True",
    "EMAIL_HOST": "smtp.gmail.com",
    "EMAIL_HOST_USER": "jaseci.dev@gmail.com",
    "EMAIL_DEFAULT_FROM": "Jaseci Admin<boyong@jaseci.org>",
    "EMAIL_HOST_PASSWORD": "yrtviyrdzmzdpjxg",
    "EMAIL_PORT": 587,
}


class email_config:
    def __init__(self, hook):
        host = email_defaults["EMAIL_HOST"]  # hook.get_glob("EMAIL_HOST")
        port = email_defaults["EMAIL_PORT"]  # int(hook.get_glob("EMAIL_PORT"))
        username = email_defaults["EMAIL_HOST_USER"]  # hook.get_glob("EMAIL_HOST_USER")
        password = email_defaults[
            "EMAIL_HOST_PASSWORD"
        ]  # hook.get_glob("EMAIL_HOST_PASSWORD")

        _use_tls = email_defaults["EMAIL_USE_TLS"]  # hook.get_glob("EMAIL_USE_TLS")
        use_tls = _use_tls.lower() == "true" if not (_use_tls is None) else False

        _sender = email_defaults[
            "EMAIL_DEFAULT_FROM"
        ]  # hook.get_glob("EMAIL_DEFAULT_FROM")
        self.sender = username if _sender is None else _sender

        context = ssl.create_default_context()

        if use_tls:
            self.server = SMTP(host, port)
            self.server.ehlo()
            self.server.starttls(context=context)
            self.server.ehlo()
        else:
            self.server = SMTP_SSL(host, port, context=context)

        self.server.login(username, password)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.server.quit()

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
