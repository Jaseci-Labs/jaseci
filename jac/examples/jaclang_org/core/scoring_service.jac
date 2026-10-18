import os;

glob USER_AGENT: str = "jaclang.org ninja leaderboard",
     MAX_TAR_BYTES: int = 52428800,
     MAX_MEMBER_BYTES: int = 2097152;

obj ScoredPayload {
    has ok: bool = False,
        error: str = "",
        meta: RepoMeta = RepoMeta(),
        an: RepoAnalysis = RepoAnalysis(),
        breakdown: ScoreBreakdown = ScoreBreakdown(),
        sha: str = "",
        service_pid: int = 0;
}

def:pub fetch_and_score(owner: str, name: str) -> ScoredPayload;
