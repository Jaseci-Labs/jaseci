glob TCSANOW: int = _TCSANOW,
     TCSADRAIN: int = _TCSADRAIN,
     TCSAFLUSH: int = _TCSAFLUSH;

glob TIOCGWINSZ: int = _TIOCGWINSZ;

glob VINTR: int = _VINTR,
     VQUIT: int = _VQUIT,
     VERASE: int = _VERASE,
     VKILL: int = _VKILL,
     VEOF: int = _VEOF,
     VTIME: int = _VTIME,
     VMIN: int = _VMIN,
     VSTART: int = _VSTART,
     VSTOP: int = _VSTOP,
     VSUSP: int = _VSUSP,
     VEOL: int = _VEOL,
     VREPRINT: int = _VREPRINT,
     VDISCARD: int = _VDISCARD,
     VWERASE: int = _VWERASE,
     VLNEXT: int = _VLNEXT,
     VEOL2: int = _VEOL2;

glob IGNBRK: int = _IGNBRK,
     BRKINT: int = _BRKINT,
     IGNPAR: int = _IGNPAR,
     PARMRK: int = _PARMRK,
     INPCK: int = _INPCK,
     ISTRIP: int = _ISTRIP,
     INLCR: int = _INLCR,
     IGNCR: int = _IGNCR,
     ICRNL: int = _ICRNL,
     IXON: int = _IXON,
     IXANY: int = _IXANY,
     IXOFF: int = _IXOFF;

glob OPOST: int = _OPOST,
     ONLCR: int = _ONLCR;

glob CSIZE: int = _CSIZE,
     CSTOPB: int = _CSTOPB,
     CREAD: int = _CREAD,
     PARENB: int = _PARENB,
     PARODD: int = _PARODD,
     CS7: int = _CS7,
     CS8: int = _CS8,
     HUPCL: int = _HUPCL;

glob ECHO: int = _ECHO,
     ECHOE: int = _ECHOE,
     ECHOK: int = _ECHOK,
     ECHONL: int = _ECHONL,
     ICANON: int = _ICANON,
     IEXTEN: int = _IEXTEN,
     ISIG: int = _ISIG,
     NOFLSH: int = _NOFLSH,
     TOSTOP: int = _TOSTOP;

def _fail(op: str) {
    raise ValueError(
        op + " failed: [Errno " + str(last_errno()) + "] " + errno_message()
    );
}

def:pub tcgetattr(fd: int) -> list[any] {
    (blob, rc) = get_attrs(fd);
    if rc != 0 {
        _fail("tcgetattr");
    }
    out: list[any] = [];
    out.append(word_at(blob, _OFF_IFLAG));
    out.append(word_at(blob, _OFF_OFLAG));
    out.append(word_at(blob, _OFF_CFLAG));
    out.append(word_at(blob, _OFF_LFLAG));
    out.append(in_speed(blob));
    out.append(out_speed(blob));
    cc: list[any] = [];
    k: int = 0;
    while k < _NCCS {
        cc.append(blob[_OFF_CC + k]);
        k += 1;
    }
    out.append(cc);
    return out;
}

def _cc_byte(e: any) -> int {
    if isinstance(e, int) {
        return e & 0xFF;
    }
    if isinstance(e, bytes) and len(e) >= 1 {
        return e[0];
    }
    raise ValueError("tcsetattr: cc entries must be int or one-byte bytes");
}

def _pack_attrs(attrs: list[any]) -> bytes {
    blob: bytes = new_buf();
    k: int = 0;
    while k < 6 {
        v = attrs[k];
        if isinstance(v, int) {
            if k == 0 {
                blob = put_word(blob, _OFF_IFLAG, v);
            } elif k == 1 {
                blob = put_word(blob, _OFF_OFLAG, v);
            } elif k == 2 {
                blob = put_word(blob, _OFF_CFLAG, v);
            } elif k == 3 {
                blob = put_word(blob, _OFF_LFLAG, v);
            }
        } else {
            raise ValueError("tcsetattr: attrs flag elements must be int");
        }
        k += 1;
    }
    speed_rc: int = set_speeds(blob, int(attrs[4]), int(attrs[5]));
    if speed_rc != 0 {
        _fail("tcsetattr");
    }
    ccv = attrs[6];
    if isinstance(ccv, list) {
        j: int = 0;
        while j < _NCCS and j < len(ccv) {
            b = _cc_byte(ccv[j]);
            blob = _put_byte(blob, _OFF_CC + j, b);
            j += 1;
        }
    } else {
        raise ValueError("tcsetattr: attrs[6] must be the cc list");
    }
    return blob;
}

def:pub tcsetattr(fd: int, when: int, attrs: list[any]) {
    if when != TCSANOW and when != TCSADRAIN and when != TCSAFLUSH {
        raise ValueError("invalid 'when' argument");
    }
    if len(attrs) != 7 {
        raise ValueError("tcsetattr: attrs must have 7 elements");
    }
    rc: int = set_attrs(fd, when, _pack_attrs(attrs));
    if rc != 0 {
        _fail("tcsetattr");
    }
}

def _put_byte(buf: bytes, off: int, value: int) -> bytes {
    return buf[:off] + value.to_bytes(1, "little") + buf[off + 1:];
}
