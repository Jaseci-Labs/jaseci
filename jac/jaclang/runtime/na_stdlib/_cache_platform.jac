def:pub platform_cache_home(home: str) -> str;

impl platform_cache_home(home: str) -> str {
    return home + "/.cache/jac";
}
