import os;
import from pathlib { Path }


enum Channel {
    STABLE = "stable",
    DEV = "dev",
    LOCAL = "local",
    EXPERIMENTAL = "experimental"
}


def local_pod_binary(project_dir: str) -> str {
    config = get_config_for_path(Path(project_dir));
    if config is None or not config.dev.pod_binary {
        return "";
    }
    base = config.project_root or Path(project_dir);
    return str(Path(base) / os.path.expanduser(config.dev.pod_binary));
}


def resolve_dev_channel(project_dir: str) -> Channel {
    if local_pod_binary(project_dir) {
        return Channel.LOCAL;
    }

    config = get_config_for_path(Path(project_dir));
    if config is None {
        return Channel.STABLE;
    }
    if config.get_section("experimental") is not None {
        return Channel.EXPERIMENTAL;
    }
    if config.get_section("dev") is None {
        return Channel.STABLE;
    }
    return Channel.DEV;
}


def resolve_experimental_pr(project_dir: str) -> str {
    config = get_config_for_path(Path(project_dir));
    if config is None {
        return "";
    }
    section = config.get_section("experimental");
    if section is None {
        return "";
    }
    return str(section.get("pr", "")).strip();
}


def resolve_pinned_spec(project_dir: str) -> str {
    config = get_config_for_path(Path(project_dir));
    if config is None {
        return "";
    }
    return config.project.jac_version;
}
