impl warn(text: str) {
    print(text, file=sys.stderr);
}

impl _suffix(detail: str) -> str {
    return " (" + detail + ")" if detail else "";
}

impl explain_bridge_error(e: BridgeError) -> int {
    where = e.app + "." + e.name;
    if isinstance(e, BridgeUnavailable) {
        warn("jacorg: " + where + " is not reachable" + _suffix(e.detail));
        warn(START_HINT);
        return EXIT_UNAVAILABLE;
    }
    if isinstance(e, BridgeTimeout) {
        warn("jacorg: " + where + " timed out" + _suffix(e.detail));
        return EXIT_TIMEOUT;
    }
    if isinstance(e, BridgeRejected) {
        warn("jacorg: " + where + " rejected the call" + _suffix(e.detail));
        warn("hint: the site wants a signed-in identity for this command");
        return EXIT_REJECTED;
    }
    warn("jacorg: " + where + " failed" + _suffix(e.detail));
    return EXIT_FAILURE;
}
