git for-each-ref --format '%(refname:short)' refs/heads | grep -v "master\|main" | xargs git branch -D
