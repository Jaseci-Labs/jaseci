import from c {
    def regcomp(preg: bytes, pattern: str, cflags: i32) -> i32;  def regexec(
        preg: bytes, string: str, nmatch: u64, pmatch: bytes, eflags: i32
    ) -> i32;  def regfree(preg: bytes);
}

glob _REG_EXTENDED: i32 = 1,
     _REG_ICASE: i32 = 2;


def:pub posix_probe -> int;


def:pub posix_compile(pat: str, icase: bool) -> bytes;


def:pub posix_exec(preg: bytes, s: str, nmatch: int, width: int) -> bytes;


def:pub pm_off(pm: bytes, width: int, i: int) -> int;


def:pub posix_free(preg: bytes);
