glob:pub I: int = 2,
     IGNORECASE: int = 2,
     L: int = 4,
     LOCALE: int = 4,
     M: int = 8,
     MULTILINE: int = 8,
     S: int = 16,
     DOTALL: int = 16,
     U: int = 32,
     UNICODE: int = 32,
     X: int = 64,
     VERBOSE: int = 64,
     A: int = 256,
     ASCII: int = 256,
     T: int = 1,
     TEMPLATE: int = 1;

enum _K: int {
    SEQ = 1,
    ALT = 2,
    CHAR = 3,
    ANY = 4,
    CLASS = 5,
    AT = 6,
    GROUP = 7,
    REP = 8,
    BACKREF = 9,
    LOOK = 10,
    FLAGS = 11
}


enum _AT: int {
    BOS = 1,
    BEG = 2,
    BEGLINE = 3,
    EOS = 4,
    END = 5,
    ENDLINE = 6,
    WB = 7,
    WNB = 8
}


enum _OP: int {
    CHAR = 1,
    ANY = 2,
    CLASS = 3,
    SPLIT = 4,
    JMP = 5,
    MARK = 6,
    JMPNZ = 7,
    SAVE = 8,
    MATCH = 9,
    BOS = 10,
    BEGLINE = 11,
    END = 12,
    ENDLINE = 13,
    EOS = 14,
    WB = 15,
    BACKREF = 16,
    FPUSH = 17,
    FPOP = 18,
    LOOK = 19
}


glob _BT_SPLIT: int = 1,
     _BT_SAVE: int = 2,
     _BT_MARK: int = 3,
     _BT_FPUSH: int = 4,
     _BT_FPOP: int = 5;

glob _MAXCP: int = 1114111;

glob _MAXPOS: int = 9223372036854775807;

glob _ESCAPE_SPECIAL: str = "()[]{}?*+-|^$\\.&~# \t\n\r\x0b\x0c";

glob _DIGIT_PRS: list[int] = [48, 57],
     _NDIGIT_PRS: list[int] = [0, 47, 58, 1114111],
     _SPACE_PRS: list[int] = [9, 13, 32, 32],
     _NSPACE_PRS: list[int] = [0, 8, 14, 31, 33, 1114111],
     _WORD_PRS: list[int] = [48, 57, 65, 90, 95, 95, 97, 122],
     _NWORD_PRS: list[int] = [0, 47, 58, 64, 91, 94, 96, 96, 123, 1114111];


obj _PS {
    has gen: int = 0,
        pregs: list[bytes] = [],
        ids: list[int] = [],
        next_id: int = 1,
        head: int = 0;
}


glob _PMW: int = posix_probe(),
     _PSX: _PS = _PS(),
     _POSIX_MAX: int = 512;


def _posix_register(preg: bytes) -> int;


def _posix_subject_ok(bv: bytes) -> bool;


def _push_prs(dst: list[int], src: list[int]);


def _in_pairs(pairs: list[int], c: int) -> bool;


def _name_index(names: dict[str, int], nm: str) -> int;


def _num_esc(cps: list[int], i: int, e: int, bp: int) -> tuple[(int, int)];


def _bounds(n: int, pos: int, endpos: int) -> tuple[(int, int)];


obj _Node {
    has kind: _K = _K.SEQ,
        ch: int = 0,
        at: _AT = _AT.BOS,
        lo: int = 0,
        hi: int = -1,
        neg: bool = False,
        greedy: bool = True,
        pairs: list[int] = [],
        kids: list[_Node] = [],
        name: str = "";
}


obj _Ins {
    has op: _OP = _OP.CHAR,
        a: int = 0,
        b: int = 0;
}


obj _Cls {
    has pairs: list[int] = [],
        neg: bool = False;
}


obj _P {
    has cps: list[int] = [],
        n: int = 0,
        i: int = 0,
        flags: int = 0,
        ngroups: int = 0,
        names: dict[str, int] = {},
        opengroups: list[int] = [],
        depth: int = 0,
        top_items: int = 0;

    def _err(msg: str, pos: int);
    def _skip_verbose;
    def _is_repeat_spec(pos: int) -> bool;
    def _rep_spec(pos: int) -> list[int];
    def _atom -> (_Node | None);
    def _piece -> (_Node | None);
    def _seq -> _Node;
    def _alt -> _Node;
    def _expect_close(open_pos: int);
    def _flagval(c: int) -> int;
    def _group -> (_Node | None);
    def _class_item(pairs: list[int]) -> int;
    def _class -> _Node;
    def _escape_atom -> _Node;
    def _parse -> _Node;
}


obj _C {
    has prog: list[_Ins] = [],
        classes: list[_Cls] = [],
        nmarks: int = 0;
}


def _emit(c: _C, op: _OP, a: int, b: int) -> int;


def _compile_node(nd: _Node, c: _C);


obj _Re {
    has prog: list[_Ins] = [],
        classes: list[_Cls] = [],
        ngroups: int = 0,
        names: dict[str, int] = {},
        nmarks: int = 0,
        flags: int = 0,
        pattern: str = "";
}


obj _St {
    has cps: list[int] = [],
        n: int = 0,
        slots: list[int] = [],
        marks: list[int] = [],
        fstack: list[int] = [],
        flags: int = 0;
}


def _bt3(stk: list[int], tag: int, x: int, y: int);


def _run(re: _Re, st: _St, pc0: int, pos0: int) -> int;


def _new_st(cps: list[int], n: int, re: _Re) -> _St;


def _reset_slots(st: _St);


obj:pub Match {
    has _re: _Re,
        string: str = "",
        _bv: bytes = b"",
        pos: int = 0,
        endpos: int = 0,
        _slots: list[int] = [];

    def init(
        _re: _Re, string: str, bv: bytes, pos: int, endpos: int, slots: list[int]
    );

    def _gtext(num: int) -> str;
    def _gnum(i: (int | str)) -> int;
    def group(i: (int | str) = 0) -> any;
    def groups(`default: any = None) -> list[any];
    def groupdict(`default: any = None) -> dict[str, any];
    def start(i: (int | str) = 0) -> int;
    def end(i: (int | str) = 0) -> int;
    def span(i: (int | str) = 0) -> tuple[(int, int)];
    def expand(template: str) -> str;
}


def _push_str(out: list[int], s: str);


def _push_range(out: list[int], pb: bytes, a: int, b: int);


def _posix_translate(pat: str, flags: int) -> (str | None);


obj:pub Pattern {
    has _re: _Re,
        pattern: str = "",
        flags: int = 0,
        groups: int = 0,
        groupindex: dict[str, int] = {},
        _preg: bytes = b"",
        _pgen: int = -1,
        _pslot: int = -1,
        _pid: int = 0,
        _posix: bool = False;

    def init(pattern: str, flags: int = 0);
    def _use_posix(bv: bytes) -> bool;
    def _posix_miss(bv: bytes, lo: int, hi: int) -> bool;
    def _scan_from(st: _St, start: int) -> int;
    def _search_from(
        string: str, bv: bytes, start: int, endpos: int
    ) -> (Match | None);

    def search(string: str, pos: int = 0, endpos: int = _MAXPOS) -> (Match | None);
    def `match(string: str, pos: int = 0, endpos: int = _MAXPOS) -> (Match | None);
    def fullmatch(string: str, pos: int = 0, endpos: int = _MAXPOS) -> (Match | None);
    def finditer(string: str, pos: int = 0, endpos: int = _MAXPOS) -> list[Match];
    def findall(string: str, pos: int = 0, endpos: int = _MAXPOS) -> list[str];
    def split(string: str, maxsplit: int = 0) -> list[any];
    def _subn(repl: str, string: str, count: int) -> tuple[(str, int)];
    def sub(repl: str, string: str, count: int = 0) -> str;
    def subn(repl: str, string: str, count: int = 0) -> tuple[(str, int)];
}


def _compile_re(pattern: str, flags: int) -> _Re;


def _expand_repl(template: str, m: Match, re: _Re) -> str;


def:pub compile(pattern: str, flags: int = 0) -> Pattern;


def:pub search(pattern: str, string: str, flags: int = 0) -> (Match | None);


def:pub `match(pattern: str, string: str, flags: int = 0) -> (Match | None);


def:pub fullmatch(pattern: str, string: str, flags: int = 0) -> (Match | None);


def:pub findall(pattern: str, string: str, flags: int = 0) -> list[str];


def:pub finditer(pattern: str, string: str, flags: int = 0) -> list[Match];


def:pub split(
    pattern: str, string: str, maxsplit: int = 0, flags: int = 0
) -> list[any];


def:pub sub(
    pattern: str, repl: str, string: str, count: int = 0, flags: int = 0
) -> str;


def:pub subn(
    pattern: str, repl: str, string: str, count: int = 0, flags: int = 0
) -> tuple[(str, int)];


def:pub escape(pattern: str) -> str;


def:pub purge;
