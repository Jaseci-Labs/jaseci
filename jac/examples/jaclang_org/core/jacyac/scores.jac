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

impl sorted_projects(projects: list[Project], query: str, sort: str) -> list[Project] {
    q = query.strip().lower();
    result = [
        p
        for p in projects
        if not q or q in (p.full + " " + p.description + " " + p.owner_username).lower()
    ];
    if sort == "stars" {
        result.sort(key=lambda (p: Project) { -p.stars; });
    } elif sort == "newest" {
        result.sort(key=lambda (p: Project) { p.added_at; }, reverse=True);
    } else {
        result.sort(key=lambda (p: Project) { (-p.score, p.full); });
    }
    return result;
}
