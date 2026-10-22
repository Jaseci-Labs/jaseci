import from "@jac/runtime" {
    jacLogin,
    jacSignup,
    __getApiBaseUrl,
    jacLogout,
    jacIsLoggedIn,
    __getLocalStorage,
    __setLocalStorage,
    __removeLocalStorage
}

obj Session {
    has loggedIn: bool,
        checking: bool,
        signup: bool,
        username: str,
        email: str,
        password: str,
        error: str,
        busy: bool,
        githubEnabled: bool,
        githubLogin: Callable[[], None],
        setUsername: Callable[[str], None],
        setEmail: Callable[[str], None],
        setPassword: Callable[[str], None],
        toggleMode: Callable[[], None],
        submit: Callable[[], None],
        logout: Callable[[], None];
}

def:pub useSession -> Session;

def:pub stored_username -> str;

async def account_handle(fallback: str) -> str;

impl account_handle(fallback: str) -> str {
    token = __getLocalStorage("jac_token");
    if not token {
        return fallback;
    }
    try {
        response = await fetch(
            __getApiBaseUrl() + "/user/me",
            {"headers": {"Authorization": "Bearer " + token}}
        );
        if not response.ok {
            return fallback;
        }
        envelope: any = await response.json();
        for ident in (envelope.data?.identities or []) {
            if ident.type == "username" and ident.value {
                return str(ident.value);
            }
        }
    } except Exception {}
    return fallback;
}

impl stored_username -> str {
    return __getLocalStorage("jacyac_username")
        or __getLocalStorage("lx_username")
        or __getLocalStorage("socialize_username")
        or "";
}

impl useSession -> Session {
    has loggedIn: bool = False,
        checking: bool = True,
        signup: bool = False,
        username: str = "",
        email: str = "",
        password: str = "",
        error: str = "",
        busy: bool = False,
        githubEnabled: bool = False;

    async def checkGithub {
        try {
            githubEnabled = await github_enabled();
        } except Exception {
            githubEnabled = False;
        }
    }
    async def githubLogin -> None {
        if busy {
            return;
        }
        busy = True;
        error = "";
        try {
            if await github_login() {
                loggedIn = True;
            }
        } except Exception as e {
            error = str(e);
        } finally {
            busy = False;
        }
    }

    can with entry {
        checkGithub();
        loggedIn = jacIsLoggedIn();
        checking = False;
    }

    async def submit -> None {
        if busy {
            return;
        }
        error = "";
        if not username.strip() or not password or (signup and not email.strip()) {
            error = "Please fill in all fields";
            return;
        }
        if signup and "@" in username {
            error = "Your username can't contain @; your email goes in the email field";
            return;
        }
        if signup and "@" not in email {
            error = "Please enter a valid email address";
            return;
        }
        busy = True;
        try {
            if signup {
                result = await jacSignup(
                    [
                        {"type": "username", "value": username.strip()},
                        {"type": "email", "value": email.strip()}
                    ],
                    password
                );
                if not result.success {
                    error = result.error or "Registration failed. Please try again.";
                    return;
                }
            }
            if await jacLogin(username.strip(), password) {
                __setLocalStorage(
                    "jacyac_username", await account_handle(username.strip())
                );
                password = "";
                loggedIn = True;
            } else {
                error = "Account created. Please log in."
                    if signup
                    else "Invalid username, email or password";
                signup = False;
            }
        } except Exception {
            error = "Could not reach the server. Please try again.";
        } finally {
            busy = False;
        }
    }

    def logout {
        jacLogout();
        for key in [
            "jacyac_username",
            "lx_username",
            "socialize_username",
            "lx_activity_total",
            "lx_welcomed"
        ] {
            __removeLocalStorage(key);
        }
        loggedIn = False;
        username = "";
        email = "";
        password = "";
        error = "";
        signup = False;
    }

    return Session(
        loggedIn=loggedIn,
        checking=checking,
        signup=signup,
        username=username,
        email=email,
        password=password,
        error=error,
        busy=busy,
        githubEnabled=githubEnabled,
        githubLogin=githubLogin,
        setUsername=lambda (value: str) { username = value; },
        setEmail=lambda (value: str) { email = value; },
        setPassword=lambda (value: str) { password = value; },
        toggleMode=lambda {
            signup = not signup;
            error = "";
        },
        submit=submit,
        logout=logout
    );
}
