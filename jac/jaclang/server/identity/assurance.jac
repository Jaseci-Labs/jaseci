import time;
import from contextvars { ContextVar }

glob AAL1: str = 'aal1',
     AAL2: str = 'aal2',
     METHOD_PASSWORD: str = 'pwd',
     METHOD_FEDERATED: str = 'sso',
     METHOD_TOTP: str = 'otp',
     METHOD_RECOVERY: str = 'recovery',
     _caller_assurance: ContextVar[dict[str, any] | None] = ContextVar(
         '_jaclang_caller_assurance', `default=None
     );


def second_factor_claims(methods: list[str]) -> dict[str, any];


def carried_claims(claims: (dict[str, any] | None)) -> dict[str, any];


def token_assurance(token: (str | None)) -> dict[str, any];


def bind_caller_assurance(claims: (dict[str, any] | None)) -> any;


def release_caller_assurance(binding: any);


def caller_assurance_level -> str;


def caller_authentication_methods -> list[str];

impl second_factor_claims(methods: list[str]) -> dict[str, any] {
    ordered: list[str] = [];
    for method in methods {
        if method and method not in ordered {
            ordered.append(str(method));
        }
    }
    return {'aal': AAL2, 'amr': ordered, 'auth_time': int(time.time())};
}


impl carried_claims(claims: (dict[str, any] | None)) -> dict[str, any] {
    if not isinstance(claims, dict) or claims.get('aal') != AAL2 {
        return {};
    }
    carried: dict[str, any] = {'aal': AAL2};
    methods = claims.get('amr');
    if isinstance(methods, list) {
        carried['amr'] = [str(m) for m in methods];
    }
    moment = claims.get('auth_time');
    if isinstance(moment, (int, float)) and not isinstance(moment, bool) {
        carried['auth_time'] = int(moment);
    }
    return carried;
}


impl token_assurance(token: (str | None)) -> dict[str, any] {
    if not token {
        return {};
    }
    try {
        decoded = jwt_decode(
            token, signing_secret(), algorithms=[signing_algorithm()], verify_exp=True
        );
    } except Exception {
        return {};
    }
    if decoded.get('type') == 'api_key' {
        return {};
    }
    return carried_claims(decoded);
}


impl bind_caller_assurance(claims: (dict[str, any] | None)) -> any {
    return _caller_assurance.set(claims);
}


impl release_caller_assurance(binding: any) {
    _caller_assurance.reset(binding);
}


impl caller_assurance_level -> str {
    claims = _caller_assurance.get();
    if claims is None {
        return '';
    }
    return AAL2 if claims.get('aal') == AAL2 else AAL1;
}


impl caller_authentication_methods -> list[str] {
    claims = _caller_assurance.get();
    if not claims {
        return [];
    }
    return [str(m) for m in (claims.get('amr') or [])];
}
