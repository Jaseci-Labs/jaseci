import from jaclang.data.contracts { JsonEndpoint }

import from urllib.parse { quote }

obj GithubRepo {
    has full: str,
        url: str,
        description: str = "",
        stars: int = 0;
}

obj GithubRepos {
    has linked: bool = False,
        login: str = "",
        repos: list[GithubRepo] = [],
        next_page: int = 0,
        error: str = "";
}

def public_api(path: str) -> bytes;

def:pub github_repositories(session_token: str, page: int = 1) -> GithubRepos;

def:protect verified_owner(full: str, session_token: str) -> bool;
