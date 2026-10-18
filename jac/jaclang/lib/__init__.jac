glob __all__ = _jaclib.__all__;

def __getattr__(name: str) -> object;

def __dir__ -> list[str];

impl __getattr__(name: str) -> object {
    return _jaclib.__getattr__(name);
}

impl __dir__ -> list[str] {
    return list(_jaclib.__dir__());
}
