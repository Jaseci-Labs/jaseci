"""
This module includes code related to configuring Jaseci's mail serving
"""
from jaseci_serv.base.models import lookup_global_config
from django.core import mail
from jaseci.utils.utils import logger


email_config_defaults = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_HOST_USER': 'prod@lifelogify.com',
    'EMAIL_DEFAULT_FROM': 'hello@jaseci.com',
    'EMAIL_HOST_PASSWORD': 'pwzaijgtrupomcjy',
    'EMAIL_PORT': 587,
}

email_template_defaults = {
    'EMAIL_ACTIVATION_SUBJ': 'Please activate your account!',
    'EMAIL_ACTIVATION_BODY': "Thank you for creating an account!\n\n"
                             "Activation Code: {{code}}\n"
                             "Please click below to activate:\n{{link}}",
    'EMAIL_ACTIVATION_HTML_BODY': "Thank you for creating an account!<br><br>"
                                  "Activation Code: {{code}}<br>"
                                  "Please click below to activate:<br>"
                                  "{{link}}",
    'EMAIL_RESETPASS_SUBJ': "Password Reset for Jaseci Account",
    'EMAIL_RESETPASS_BODY': "Your Jaseci password reset token is: {{token}}",
    'EMAIL_RESETPASS_HTML_BODY': "Your Jaseci password reset"
                                 "token is: {{token}}",
}


class email_config():
    def __init__(self):
        self.setup_email_connection()  # creates self.connection
        self.setup_email_templates()

    def setup_email_connection(self):
        """Loads an email connection relative to global configs"""
        def resolve(name):
            return lookup_global_config(name=name,
                                        default=email_config_defaults[name])
        backend = resolve('EMAIL_BACKEND')
        host = resolve('EMAIL_HOST')
        port = int(resolve('EMAIL_PORT'))
        username = resolve('EMAIL_HOST_USER')
        password = resolve('EMAIL_HOST_PASSWORD')
        use_tls = bool(resolve('EMAIL_USE_TLS'))
        self.sender = resolve('EMAIL_DEFAULT_FROM')

        self.connection = mail.get_connection(
            backend=backend, host=host, port=port,
            username=username, password=password,
            use_tls=use_tls)

    def setup_email_templates(self):
        """Loads email content templates from global config"""
        def resolve(name):
            return lookup_global_config(name=name,
                                        default=email_template_defaults[name])
        self.activ_subj = resolve('EMAIL_ACTIVATION_SUBJ')
        self.activ_body = resolve('EMAIL_ACTIVATION_BODY')
        if('{{code}}' not in self.activ_body and
           '{{link}}' not in self.activ_body):
            logger.error("{{code/link}} must be present in email template")
            self.activ_body = email_template_defaults['EMAIL_ACTIVATION_BODY']
        self.activ_html = resolve('EMAIL_ACTIVATION_HTML_BODY')
        if('{{code}}' not in self.activ_html and
           '{{link}}' not in self.activ_html):
            logger.error("{{code/link}} must be present in email template")
            self.activ_body = email_template_defaults[
                'EMAIL_ACTIVATION_HTML_BODY']
        self.reset_subj = resolve('EMAIL_RESETPASS_SUBJ')
        self.reset_body = resolve('EMAIL_RESETPASS_BODY')
        if('{{token}}' not in self.reset_body):
            logger.error("{{token}} must be present in email template")
            self.reset_body = email_template_defaults['EMAIL_RESETPASS_BODY']
        self.reset_html = resolve('EMAIL_RESETPASS_HTML_BODY')
        if('{{token}}' not in self.reset_html):
            logger.error("{{token}} must be present in email template")
            self.reset_html = email_template_defaults[
                'EMAIL_RESETPASS_HTML_BODY']

    def send_activation_email(self, email, code, link):
        """Apply relevant parameters to loaded templates"""
        body = self.activ_body.replace(
            '{{code}}', code).replace('{{link}}', link)
        html = self.activ_html.replace(
            '{{code}}', code).replace('{{link}}', link)
        with self.connection as connection:
            msg = mail.EmailMultiAlternatives(
                subject=self.activ_subj,
                body=body,
                from_email=self.sender,
                to=[email],
                connection=connection,
            )
            msg.attach_alternative(html, "text/html")
            msg.send(fail_silently=False)

    def send_reset_email(self, email, token):
        """Apply relevant parameters to loaded templates"""
        body = self.reset_body.replace('{{token}}', token)
        html = self.reset_html.replace('{{token}}', token)
        with self.connection as connection:
            msg = mail.EmailMultiAlternatives(
                subject=self.reset_subj,
                body=body,
                from_email=self.sender,
                to=[email],
                connection=connection,
            )
            msg.attach_alternative(html, "text/html")
            msg.send(fail_silently=False)
