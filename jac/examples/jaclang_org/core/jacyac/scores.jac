import from "@jac/runtime" { __getLocalStorage }

obj Scores {
    has query: str,
        sort: str,
        projects: list[Project],
        repos: list[GithubRepo],
        githubLogin: str,
        githubLinked: bool,
        reposLoading: bool,
        reposError: str,
        nextPage: int,
        setQuery: Callable[[str], None],
        setSort: Callable[[str], None],
        loadRepos: Callable[[int], None];
}

def sorted_projects(projects: list[Project], query: str, sort: str) -> list[Project];

def:pub useScores(model: JacYacState) -> Scores;
