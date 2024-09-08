# **`MAIL SERVICE CONFIG`**


## `Version 1`
### `Structure`
```js
EMAIL_ACTIVATION_BODY= "Thank you for creating an account!\n\nActivation Code: {{code}}\nPlease click below to activate:\n{{link}}"
EMAIL_ACTIVATION_HTML_BODY= "Thank you for creating an account!<br><br>Activation Code: {{code}}<br>Please click below to activate:<br>{{link}}"
EMAIL_ACTIVATION_SUBJ= "Thank you for creating an account!\n\n"
EMAIL_DEFAULT_FROM= "{{some values}}"
EMAIL_HOST= "{{some values}}"
EMAIL_HOST_PASSWORD= "{{some values}}"
EMAIL_HOST_USER= "{{some values}}"
EMAIL_PORT= "{{some values}}"
EMAIL_RESETPASS_BODY= "Your Jaseci password reset token is: {{token}}"
EMAIL_RESETPASS_HTML_BODY= "Your Jaseci password reset" "token is: {{token}}"
EMAIL_RESETPASS_SUBJ= "Password Reset for Jaseci Account"
EMAIL_USE_TLS= True
```
- one key per attribute

---

## `Version 2` (**Current Implementation**)
### `Structure`
```js
MAIL_CONFIG = {
    "enabled": True,
    "quiet": True,
    "version": 2,
    "tls": True,
    "host": "",
    "port": 587,
    "sender": "",
    "user": "",
    "pass": "",
    "backend": "smtp",
    "templates": {
        "activation_subj": "Please activate your account!",
        "activation_body": "Thank you for creating an account!\n\nActivation Code: {{code}}\nPlease click below to activate:\n{{link}}",
        "activation_html_body": "Thank you for creating an account!<br><br>Activation Code: {{code}}<br>Please click below to activate:<br>{{link}}",
        "resetpass_subj": "Password Reset for Jaseci Account",
        "resetpass_body": "Your Jaseci password reset token is: {{token}}",
        "resetpass_html_body": "Your Jaseci password reset" "token is: {{token}}",
    },
    // optional
    "migrate": false
}
```
- Backward compatible with `version 1`
- `version` attribute will determine which version should be used
    - `version: 2`
        - this will use the actual `MAIL_CONFIG` values including the templates
    - `version: 1`
        - this will override `MAIN_CONFIG`'s attribute (**but not saved!!**).
        - Values from `Version 1` will be copied to their equivalent `Version 2` attributes.
- `migrate`
    - if this field is true. `Version 1` values will be copied to their equivalent `Version 2` attributes and it will be saved on DB
