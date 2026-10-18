import json;
import re;

glob USER_AGENT: str = "jaclang.org cli scorer",
     MAX_TAR_BYTES: int = 52428800,
     MAX_MEMBER_BYTES: int = 2097152;

glob ERROR_TEXT: dict[str, str] = {
         "bad_ref": "expected owner/name or a github.com URL",
         "not_found": "GitHub knows no such repo (a private repo and a rate limit look the same; set GITHUB_TOKEN)",
         "fetch_failed": "could not download the default-branch tarball (over 50 MB, or GitHub is unreachable)",
         "not_jac": "no .jac files on the default branch, so there is nothing to score"
     };

obj ScoreResult {
    has ok: bool = False,
        error: str = "",
        meta: RepoMeta = RepoMeta(),
        an: RepoAnalysis = RepoAnalysis(),
        breakdown: ScoreBreakdown = ScoreBreakdown(),
        sha: str = "";
}

def parse_repo_ref(text: str) -> tuple[str, str] | None;

def score_repo(owner: str, name: str, quiet: bool = False) -> ScoreResult;

def as_dict(res: ScoreResult) -> dict[str, object];

def render(res: ScoreResult) -> str;

def run_score(repo: str, as_json: bool) -> int;
