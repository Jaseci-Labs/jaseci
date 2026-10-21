import hashlib;
import os;
import re;
import from pathlib { Path }
import from jaclang.cli.guide_store { nav_pages, parse_guide }

obj NavEntry {
    has page: str = "",
        title: str = "",
        order: int = 0;
}

obj DocBundle {
    has pages: dict[str, str] = {},
        nav: dict[str, NavEntry] = {},
        jac_version: str = "",
        fingerprint: str = "";
}

def label_of(version: str) -> str;

def bundle_from(ddir: Path, jac_version: str) -> DocBundle;

impl label_of(version: str) -> str {
    m = re.`match(r"^v?(\d+)\.(\d+)", version.strip());
    if not m {
        return "dev";
    }
    return "v" + (m.group(1) as str) + "." + (m.group(2) as str);
}

impl bundle_from(ddir: Path, jac_version: str) -> DocBundle {
    bundle = DocBundle(jac_version=jac_version);
    digest = hashlib.sha1(jac_version.encode("utf-8"));
    for path in sorted(ddir.rglob("*.md"), key=lambda (p: Path) { str(p); }) {
        rel = str(path.relative_to(ddir)).replace(os.sep, "/");
        g = parse_guide(path);
        if g is None {
            continue;
        }
        bundle.pages[rel] = g.body;
        digest.update(rel.encode("utf-8"));
        digest.update(g.body.encode("utf-8"));
    }
    for np in nav_pages(ddir) {
        bundle.nav[np.page] = NavEntry(page=np.page, title=np.title, order=np.order);
        digest.update((np.page + "\x00" + np.title).encode("utf-8"));
    }
    bundle.fingerprint = digest.hexdigest();
    return bundle;
}
