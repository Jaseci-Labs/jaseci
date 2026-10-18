glob _active: list[any] = [AuthSettings(), '', None];


def configure_identity(settings: AuthSettings, base_path: str);

def auth_settings -> AuthSettings;

def signing_secret -> str;

def signing_algorithm -> str;

def token_ttl_days -> int;

def password_hash_cost -> int;

impl configure_identity(settings: AuthSettings, base_path: str) {
    _active[0] = settings;
    _active[1] = base_path;
    _active[2] = None;
}

impl auth_settings -> AuthSettings {
    return _active[0];
}

impl signing_secret -> str {
    cached = _active[2];
    if cached {
        return str(cached);
    }
    settings: AuthSettings = _active[0];
    secret = settings.resolve_secret(str(_active[1] or ''));
    _active[2] = secret;
    return secret;
}

impl signing_algorithm -> str {
    return auth_settings().algorithm;
}

impl token_ttl_days -> int {
    return auth_settings().token_ttl_days;
}

impl password_hash_cost -> int {
    return auth_settings().password.hash_cost;
}
