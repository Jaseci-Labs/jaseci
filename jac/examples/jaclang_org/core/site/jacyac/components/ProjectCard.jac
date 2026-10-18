import from "lucide-react" {
    Star,
    GitFork,
    ExternalLink,
    Trash2,
    RefreshCw,
    AlertTriangle,
    FolderGit2
}

def:pub ProjectCard(
    project: Project,
    isMine: bool,
    showOwner: bool,
    avatars: dict[str, str],
    busy: bool,
    onRemove: Callable[[str], None],
    onRescore: Callable[[str], None],
    onViewOwner: Callable[[str], None],
) -> JsxElement;
