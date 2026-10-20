import from "lucide-react" { Users, FolderGit2 }

def:pub ExploreTab(
    mode: str,
    onModeChange: Callable[[str], None],
    allProfiles: list[Profile],
    followingIds: list[str],
    myProfileId: str,
    avatars: dict[str, str],
    projects: list[Project],
    projectsLoading: bool,
    onFollow: Callable[[str], None],
    onUnfollow: Callable[[str], None],
    onViewProfile: Callable[[str], None],
) -> JsxElement;
