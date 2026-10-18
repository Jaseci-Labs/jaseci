impl code_sample(files: dict[str, str]) -> str {
    chunks: list[str] = [];
    remaining = 6000;
    paths = sorted(files.keys());
    paths = [
        p
        for p in paths
        if p.endswith(".jac")
    ]
        + [
            p
            for p in paths
            if p.lower().endswith("readme.md") or p.endswith("jac.toml")
        ];
    for path in paths[:8] {
        chunk = (path[:180] + "\n" + files[path][:1000])[:remaining];
        chunks.append(chunk);
        remaining -= len(chunk) + 2;
        if remaining <= 0 {
            break;
        }
    }
    return "\n\n".join(chunks);
}

impl optional_review(files: dict[str, str]) -> CodeReview | None {
    try {
        return review_sample(code_sample(files));
    } except Exception {
        return None;
    }
}
