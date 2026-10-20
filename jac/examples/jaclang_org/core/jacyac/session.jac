import from "@jac/runtime" {
    jacLogin,
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
        password: str,
        error: str,
        busy: bool,
        githubEnabled: bool,
        githubLogin: Callable[[], None],
        setUsername: Callable[[str], None],
        setPassword: Callable[[str], None],
        toggleMode: Callable[[], None],
        submit: Callable[[], None],
        logout: Callable[[], None];
}

def:pub useSession -> Session;

def:pub stored_username -> str;

impl stored_username -> str {
    return __getLocalStorage("jacyac_username")
        or __getLocalStorage("lx_username")
        or __getLocalStorage("socialize_username")
        or "";
}
