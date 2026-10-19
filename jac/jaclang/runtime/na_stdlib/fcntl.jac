glob F_GETFL: int = _F_GETFL,
     F_SETFL: int = _F_SETFL,
     F_GETFD: int = _F_GETFD,
     F_SETFD: int = _F_SETFD,
     F_SETOWN: int = _F_SETOWN;

glob O_NONBLOCK: int = _O_NONBLOCK,
     O_APPEND: int = _O_APPEND,
     O_ASYNC: int = _O_ASYNC;

def:pub fcntl(fd: int, cmd: int, arg: int = 0) -> int {
    rc: int = do_fcntl(fd, cmd, arg);
    if rc < 0 {
        raise ValueError(
            "fcntl failed: [Errno " + str(last_errno()) + "] " + errno_message()
        );
    }
    return rc;
}

def:pub ioctl(fd: int, request: int, arg: bytes) -> bytes {
    rc: int = do_ioctl(fd, request, arg);
    if rc < 0 {
        raise ValueError(
            "ioctl failed: [Errno " + str(last_errno()) + "] " + errno_message()
        );
    }
    return arg;
}
