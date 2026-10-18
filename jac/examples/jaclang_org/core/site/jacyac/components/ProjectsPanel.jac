import from "lucide-react" { FolderGit2, Plus, AlertCircle, CheckCircle2 }

def:pub ProjectsPanel(
    projects: list[Project],
    isMine: bool,
    avatars: dict[str, str],
    busy: bool,
    error: str,
    notice: str,
    onAdd: Callable[[str], None],
    onRemove: Callable[[str], None],
    onRescore: Callable[[str], None],
    onViewOwner: Callable[[str], None],
) -> JsxElement;
