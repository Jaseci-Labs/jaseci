################################################
#                   DEFAULTS                   #
################################################

MAIL_ERR_MSG = "Mail service is disabled or not yet configured!"
MAIL_CONFIG = {
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
