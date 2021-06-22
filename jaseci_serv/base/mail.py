"""
This module includes code related to configuring Jaseci's mail serving
"""
from base.models import lookup_global_config
from django.core import mail

email_defaults = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_HOST_USER': 'prod@lifelogify.com',
    'EMAIL_HOST_PASSWORD': 'pwzaijgtrupomcjy',
    'EMAIL_PORT': 587,
}


def load_email_connection():
    """Loads an email connection relative to global configs"""
    def resolve(name):
        return lookup_global_config(name=name, default=email_defaults[name])
    backend = resolve('EMAIL_BACKEND')
    host = resolve('EMAIL_HOST')
    port = int(resolve('EMAIL_PORT'))
    username = resolve('EMAIL_HOST_USER')
    password = resolve('EMAIL_HOST_PASSWORD')
    use_tls = bool(resolve('EMAIL_USE_TLS'))

    return mail.get_connection(backend=backend, host=host, port=port,
                               username=username, password=password,
                               use_tls=use_tls)
