import from "lucide-react" {
    MapPin,
    Link2,
    Github,
    CalendarDays,
    Camera,
    Trash2,
    Pencil
}

def:pub ProfileHeader(
    bundle: ProfileBundle,
    isMine: bool,
    avatars: dict[str, str],
    isFollowing: bool,
    onFollow: Callable[[str], None],
    onUnfollow: Callable[[str], None],
    onStartEdit: Callable[[], None],
    avatarBusy: bool,
    onAvatarFile: Callable[[any], None],
    onClearAvatar: Callable[[], None],
) -> JsxElement;
