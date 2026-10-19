glob POLLIN: int = _POLLIN,
     POLLOUT: int = _POLLOUT,
     POLLERR: int = _POLLERR,
     POLLHUP: int = _POLLHUP,
     POLLNVAL: int = _POLLNVAL;

def _check_fd(fd: int);

def _add_fds(lst: list[int], events: int, fds: list[int], masks: list[int]);

def:pub select(
    rlist: list[int], wlist: list[int], xlist: list[int], timeout: (float | None) = -1.0
) -> tuple[(list[int], list[int], list[int])];

impl _check_fd(fd: int) {
    if fd < 0 or fd >= _FD_SETSIZE {
        raise ValueError("filedescriptor out of range in select()");
    }
}

impl _add_fds(lst: list[int], events: int, fds: list[int], masks: list[int]) {
    for fd in lst {
        _check_fd(fd);
        found: bool = False;
        k: int = 0;
        while k < len(fds) {
            if fds[k] == fd {
                masks[k] = masks[k] | events;
                found = True;
                break;
            }
            k += 1;
        }
        if not found {
            fds.append(fd);
            masks.append(events);
        }
    }
}

impl select(
    rlist: list[int], wlist: list[int], xlist: list[int], timeout: (float | None) = -1.0
) -> tuple[(list[int], list[int], list[int])] {
    fds: list[int] = [];
    masks: list[int] = [];

    _add_fds(rlist, _POLLIN | _POLLERR, fds, masks);
    _add_fds(wlist, _POLLOUT | _POLLERR, fds, masks);
    for fd in xlist {
        _check_fd(fd);
    }

    tmo: int = -1;
    if timeout is None {
        tmo = -1;
    } elif timeout >= 0.0 {
        tmo = int(timeout * 1000.0);
    } elif timeout != -1.0 {
        raise ValueError("timeout must be None, -1.0 (block), or non-negative");
    }
    res: list[int] = do_poll(fds, masks, tmo);
    if res[0] < 0 {
        raise ValueError(
            "poll failed: [Errno " + str(last_errno()) + "] " + errno_message()
        );
    }
    out_r: list[int] = [];
    out_w: list[int] = [];
    out_x: list[int] = [];
    n: int = len(fds);
    k: int = 0;
    while k < n {
        rev: int = res[k + 1];
        if (rev & _POLLNVAL) != 0 {
            raise ValueError("invalid file descriptor in select()");
        }
        if rev != 0 {
            fd: int = fds[k];
            if (rev & (_POLLIN | _POLLERR | _POLLHUP)) != 0 {
                out_r.append(fd);
            }
            if (rev & (_POLLOUT | _POLLERR | _POLLHUP)) != 0 {
                out_w.append(fd);
            }
        }
        k += 1;
    }
    return (out_r, out_w, out_x);
}
