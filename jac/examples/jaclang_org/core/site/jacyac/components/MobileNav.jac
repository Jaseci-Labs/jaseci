import from "lucide-react" { Home, Compass, Hash, User }

def:pub MobileNav(
    activeTab: str, notifCount: int, onNavigate: Callable[[str], None]
) -> JsxElement;
