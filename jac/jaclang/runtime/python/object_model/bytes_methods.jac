"""Shared bytes and bytearray methods: Objects/bytes_methods.c and the byte
instantiation of Objects/stringlib in native Jac.

The `_Py_bytes_*` functions and the shared `_Py_*__doc__` strings are defined
here under their C names, as bytes_methods.c exports them, so bytes,
bytearray and every C caller use them unchanged. The stringlib templates that
bytesobject.c and bytearrayobject.c both instantiate for `char`
(fastsearch.h, count.h, find.h, find_max_char.h, split.h, partition.h,
join.h, ctype.h, transmogrify.h and its clinic glue) are one copy of `bl_*`
definitions over raw bytes that both types call. Where the two
instantiations differ (STRINGLIB_NEW, STRINGLIB_MUTABLE,
STRINGLIB_CHECK_EXACT, STRINGLIB_GET_EMPTY), the object at hand decides: an
instance of bytes or a bytes subclass takes bytesobject.c's immutable paths,
any other object bytearrayobject.c's. The ASCII classes of Include/pyctype.h
are tested inline; `_Py_ctype_table` and its case tables stay in
Python/pyctype.c. The search keeps fastsearch.h's three algorithms (the
default bloom-filtered Horspool scan, the Crochemore-Perrin two-way search
and the adaptive switch between them) and their thresholds. See
../LICENSE.cpython.
"""

import from c {
    def memchr(source: ptr, value: i32, size: u64) -> ptr;  def memcmp(
        left: ptr, right: ptr, size: u64
    ) -> i32;  def memcpy(target: ptr, source: ptr, size: u64) -> ptr;  def memset(
        target: ptr, value: i32, size: u64
    ) -> ptr;  def PyByteArray_FromStringAndSize(
        data: ptr[u8], size: i64
    ) -> ptr[PyObject];
    # The shared docstrings of pycore_bytes_methods.h (PyDoc_STRVAR_shared):
    # NUL-terminated char arrays, as C defines them.
    glob _Py_isspace__doc__: list[u8] = (
             b"B.isspace() -> bool\n\n"
             b"Return True if all characters in B are whitespace\n"
             b"and there is at least one character in B, False otherwise.\0"
         ),
         _Py_isalpha__doc__: list[u8] = (
             b"B.isalpha() -> bool\n\n"
             b"Return True if all characters in B are alphabetic\n"
             b"and there is at least one character in B, False otherwise.\0"
         ),
         _Py_isalnum__doc__: list[u8] = (
             b"B.isalnum() -> bool\n\n"
             b"Return True if all characters in B are alphanumeric\n"
             b"and there is at least one character in B, False otherwise.\0"
         ),
         _Py_isdigit__doc__: list[u8] = (
             b"B.isdigit() -> bool\n\n"
             b"Return True if all characters in B are digits\n"
             b"and there is at least one character in B, False otherwise.\0"
         ),
         _Py_islower__doc__: list[u8] = (
             b"B.islower() -> bool\n\n"
             b"Return True if all cased characters in B are lowercase and there is\n"
             b"at least one cased character in B, False otherwise.\0"
         ),
         _Py_isupper__doc__: list[u8] = (
             b"B.isupper() -> bool\n\n"
             b"Return True if all cased characters in B are uppercase and there is\n"
             b"at least one cased character in B, False otherwise.\0"
         ),
         _Py_istitle__doc__: list[u8] = (
             b"B.istitle() -> bool\n\n"
             b"Return True if B is a titlecased string and there is at least one\n"
             b"character in B, i.e. uppercase characters may only follow uncased\n"
             b"characters and lowercase characters only cased ones. Return False\n"
             b"otherwise.\0"
         ),
         _Py_lower__doc__: list[u8] = (
             b"B.lower() -> copy of B\n\n"
             b"Return a copy of B with all ASCII characters converted to lowercase.\0"
         ),
         _Py_upper__doc__: list[u8] = (
             b"B.upper() -> copy of B\n\n"
             b"Return a copy of B with all ASCII characters converted to uppercase.\0"
         ),
         _Py_title__doc__: list[u8] = (
             b"B.title() -> copy of B\n\n"
             b"Return a titlecased version of B, i.e. ASCII words start with\n"
             b"uppercase characters, all remaining cased characters have lowercase.\0"
         ),
         _Py_capitalize__doc__: list[u8] = (
             b"B.capitalize() -> copy of B\n\n"
             b"Return a copy of B with only its first character capitalized (ASCII)\n"
             b"and the rest lower-cased.\0"
         ),
         _Py_swapcase__doc__: list[u8] = (
             b"B.swapcase() -> copy of B\n\n"
             b"Return a copy of B with uppercase ASCII characters converted\n"
             b"to lowercase ASCII and vice versa.\0"
         ),
         _Py_maketrans__doc__: list[u8] = (
             b"B.maketrans(frm, to) -> translation table\n\n"
             b"Return a translation table (a bytes object of length 256) suitable\n"
             b"for use in the bytes or bytearray translate method where each byte\n"
             b"in frm is mapped to the byte at the same position in to.\n"
             b"The bytes objects frm and to must be of the same length.\0"
         ),
         _Py_isascii__doc__: list[u8] = (
             b"B.isascii() -> bool\n\n"
             b"Return True if B is empty or all characters in B are ASCII,\n"
             b"False otherwise.\0"
         ),
         # The clinic docstrings of stringlib/clinic/transmogrify.h.h. C
         # makes a static copy in each including file; here both types'
         # method tables share these.
         stringlib_expandtabs__doc__: list[u8] = (
             b"expandtabs($self, /, tabsize=8)\n--\n\n"
             b"Return a copy where all tab characters are expanded using spaces.\n\n"
             b"If tabsize is not given, a tab size of 8 characters is assumed.\0"
         ),
         stringlib_ljust__doc__: list[u8] = (
             b"ljust($self, width, fillchar=b' ', /)\n--\n\n"
             b"Return a left-justified string of length width.\n\n"
             b"Padding is done using the specified fill character.\0"
         ),
         stringlib_rjust__doc__: list[u8] = (
             b"rjust($self, width, fillchar=b' ', /)\n--\n\n"
             b"Return a right-justified string of length width.\n\n"
             b"Padding is done using the specified fill character.\0"
         ),
         stringlib_center__doc__: list[u8] = (
             b"center($self, width, fillchar=b' ', /)\n--\n\n"
             b"Return a centered string of length width.\n\n"
             b"Padding is done using the specified fill character.\0"
         ),
         stringlib_zfill__doc__: list[u8] = (
             b"zfill($self, width, /)\n--\n\n"
             b"Pad a numeric string with zeros on the left, to fill a field of the given width.\n\n"
             b"The original string is never truncated.\0"
         );
}

# FASTSEARCH's modes.
glob BL_FAST_COUNT: i64 = 0,
     BL_FAST_SEARCH: i64 = 1,
     BL_FAST_RSEARCH: i64 = 2;

glob:priv PY_SSIZE_T_MAX: i64 = 0x7FFFFFFFFFFFFFFF,
     # STRINGLIB_FAST_MEMCHR is memchr: find_char hands longer runs to it.
     MEMCHR_CUT_OFF: i64 = 15,
     # STRINGLIB_BLOOM_WIDTH is 64 (LONG_BIT): a byte's low 6 bits pick its bit.
     BLOOM_BITS: u64 = u64(63),
     # TABLE_SIZE_BITS 6: the two-way bad-character table has 64 entries.
     TABLE_SIZE: i64 = 64,
     TABLE_MASK: u8 = u8(63),
     # SHIFT_TYPE is uint8_t.
     MAX_SHIFT: i64 = 255,
     # split.h preallocates this many list slots.
     MAX_PREALLOC: i64 = 12,
     # sizeof(Py_buffer) on every supported (LP64) target.
     PY_BUFFER_SIZE: i64 = 80,
     # join.h releases the GIL to copy results at least this long.
     GIL_THRESHOLD: i64 = 1048576,
     # find_max_char: a size_t with any byte's high bit set.
     UCS1_ASCII_CHAR_MASK: u64 = u64(0x8080808080808080),
     # transmogrify.h's ljust, rjust and center share one argument parser.
     JUST_LEFT: i64 = 0,
     JUST_RIGHT: i64 = 1,
     JUST_CENTER: i64 = 2,
     CHAR_TAB: u8 = u8(9),
     CHAR_NEWLINE: u8 = u8(10),
     CHAR_RETURN: u8 = u8(13),
     CHAR_SPACE: u8 = u8(32),
     CHAR_PLUS: u8 = u8(43),
     CHAR_MINUS: u8 = u8(45),
     CHAR_ZERO: u8 = u8(48);

glob:priv expandtabs_signature = CallSignature(
         "expandtabs", ["tabsize"], 0, 1, 0, parser=PARSE_KEYWORDS
     );

# Include/pyctype.h over the C locale: _Py_ctype_table marks exactly these
# ASCII classes, and bytes at 0x80 and above belong to none.

"""Py_ISSPACE: space, tab, newline, vertical tab, form feed or return."""
def py_isspace(c: u8) -> bool {
    return c == CHAR_SPACE or (c >= CHAR_TAB and c <= CHAR_RETURN);
}

"""Py_ISLOWER."""
def py_islower(c: u8) -> bool {
    return c >= u8(97) and c <= u8(122);
}

"""Py_ISUPPER."""
def py_isupper(c: u8) -> bool {
    return c >= u8(65) and c <= u8(90);
}

"""Py_ISALPHA."""
def py_isalpha(c: u8) -> bool {
    return py_islower(c) or py_isupper(c);
}

"""Py_ISDIGIT."""
def py_isdigit(c: u8) -> bool {
    return c >= CHAR_ZERO and c <= u8(57);
}

"""Py_ISALNUM."""
def py_isalnum(c: u8) -> bool {
    return py_isalpha(c) or py_isdigit(c);
}

"""Py_ISXDIGIT: a digit or a to f in either case."""
def py_isxdigit(c: u8) -> bool {
    return py_isdigit(c)
        or (c >= u8(65) and c <= u8(70))
        or (c >= u8(97) and c <= u8(102));
}

"""Py_TOLOWER (_Py_ctype_tolower)."""
def py_tolower(c: u8) -> u8 {
    if py_isupper(c) {
        return c + u8(32);
    }
    return c;
}

"""Py_TOUPPER (_Py_ctype_toupper)."""
def py_toupper(c: u8) -> u8 {
    if py_islower(c) {
        return c - u8(32);
    }
    return c;
}

"""STRINGLIB_ISLINEBREAK."""
def is_linebreak(c: u8) -> bool {
    return c == CHAR_NEWLINE or c == CHAR_RETURN;
}

def byte_at(s: ptr[u8], i: i64) -> u8 {
    return (s + i).view(1)[0];
}

def set_byte(s: ptr[u8], i: i64, c: u8) {
    (s + i).view(1)[0] = c;
}

"""The distance in bytes from `start` to `stop`."""
def span(start: ptr[u8], stop: ptr[u8]) -> i64 {
    return i64(int(stop) - int(start));
}

"""Py_MAX."""
def imax(a: i64, b: i64) -> i64 {
    return a if a > b else b;
}

"""Py_MIN."""
def imin(a: i64, b: i64) -> i64 {
    return a if a < b else b;
}

"""The address of entry `i` in an array of Py_buffer."""
def buffer_at(buffers: ptr[u8], i: i64) -> ptr[Py_buffer] {
    return ptr[Py_buffer](buffers + i * PY_BUFFER_SIZE);
}

"""A zeroed Py_buffer on the heap (C keeps it on the stack), or NULL with
MemoryError set."""
def new_buffer_slot -> ptr[Py_buffer] {
    view = ptr[Py_buffer](PyMem_Calloc(1, u64(PY_BUFFER_SIZE)));
    if not view {
        PyErr_NoMemory();
    }
    return view;
}

"""PyBuffer_Release on a slot from new_buffer_slot, then free the slot."""
def release_buffer_slot(view: ptr[Py_buffer]) {
    PyBuffer_Release(view);
    PyMem_Free(ptr(view));
}

# The two instantiations

"""STRINGLIB_MUTABLE for `op`: bytes and its subclasses are the immutable
instantiation (bytesobject.c), anything else the bytearray one."""
def bl_mutable(op: ptr[PyObject]) -> bool {
    return not type_has_feature(object_type(op), Py_TPFLAGS_BYTES_SUBCLASS);
}

"""STRINGLIB_STR: PyBytes_AS_STRING or PyByteArray_AS_STRING."""
def bl_str(op: ptr[PyObject]) -> ptr[u8] {
    if bl_mutable(op) {
        return PyByteArray_AsString(op);
    }
    return PyBytes_AsString(op);
}

"""STRINGLIB_LEN: both types keep their length in ob_size."""
def bl_len(op: ptr[PyObject]) -> i64 {
    return object_size(op);
}

"""STRINGLIB_NEW: a new bytearray (mutable) or bytes of `n` bytes copied
from `s`, uninitialized when `s` is NULL."""
def bl_new(mutable: bool, s: ptr[u8], n: i64) -> ptr[PyObject] {
    if mutable {
        return PyByteArray_FromStringAndSize(s, n);
    }
    return PyBytes_FromStringAndSize(s, n);
}

"""STRINGLIB_CHECK_EXACT of the immutable instantiation: PyBytes_CheckExact."""
def bytes_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, ptr[PyTypeObject](addressof(PyBytes_Type)));
}

"""PyByteArray_Check."""
def bytearray_check(op: ptr[PyObject]) -> bool {
    return object_type_check(op, ptr[PyTypeObject](addressof(PyByteArray_Type)));
}

"""STRINGLIB_GET_EMPTY (bytes_get_empty), as a new reference to the empty
bytes singleton."""
def bytes_get_empty -> ptr[PyObject] {
    return PyBytes_FromStringAndSize(ptr[u8](), 0);
}

"""ADJUST_INDICES: clip slice bounds `start` and `end` to a length `n`
sequence, counting negative ones from the end."""
def bl_adjust_indices(start: i64, end: i64, n: i64) -> tuple[i64, i64] {
    lo = start;
    hi = end;
    if hi > n {
        hi = n;
    } elif hi < 0 {
        hi += n;
        if hi < 0 {
            hi = 0;
        }
    }
    if lo < 0 {
        lo += n;
        if lo < 0 {
            lo = 0;
        }
    }
    return (lo, hi);
}

# stringlib/fastsearch.h

"""STRINGLIB_BLOOM_ADD."""
def bloom_add(mask: u64, ch: u8) -> u64 {
    return mask | wrapping_shl(u64(1), u64(ch) & BLOOM_BITS);
}

"""STRINGLIB_BLOOM: whether `ch` may be in the set `mask` describes."""
def bloom(mask: u64, ch: u8) -> bool {
    return (mask & wrapping_shl(u64(1), u64(ch) & BLOOM_BITS)) != u64(0);
}

"""The index of the first `ch` in s[0:n], or -1."""
def bl_find_char(s: ptr[u8], n: i64, ch: u8) -> i64 {
    if n > MEMCHR_CUT_OFF {
        found = memchr(ptr(s), i32(ch), u64(n));
        if found.is_null() {
            return -1;
        }
        return span(s, ptr[u8](found));
    }
    i: i64 = 0;
    while i < n {
        if byte_at(s, i) == ch {
            return i;
        }
        i += 1;
    }
    return -1;
}

"""The index of the last `ch` in s[0:n], or -1. The scan is by hand on every
target (C takes memrchr past 15 bytes where the C library has it)."""
def bl_rfind_char(s: ptr[u8], n: i64, ch: u8) -> i64 {
    i = n;
    while i > 0 {
        i -= 1;
        if byte_at(s, i) == ch {
            return i;
        }
    }
    return -1;
}

"""_lex_search: the start of the lexicographically maximal suffix of the
needle (with the alphabet reversed when `invert_alphabet`), and the period
of that right half, as (max_suffix, period)."""
def bl_lex_search(
    needle: ptr[u8], len_needle: i64, invert_alphabet: bool
) -> tuple[i64, i64] {
    max_suffix: i64 = 0;
    candidate: i64 = 1;
    k: i64 = 0;
    # The period of the right half.
    period: i64 = 1;
    while candidate + k < len_needle {
        # each loop increases candidate + k + max_suffix
        a = byte_at(needle, candidate + k);
        b = byte_at(needle, max_suffix + k);
        # check if the suffix at candidate is better than max_suffix
        fell_short = (b < a) if invert_alphabet else (a < b);
        if fell_short {
            # Fell short of max_suffix. The next k + 1 characters are
            # non-increasing from candidate, so they won't start a maximal
            # suffix.
            candidate += k + 1;
            k = 0;
            # We've ruled out any period smaller than what's been scanned
            # since max_suffix.
            period = candidate - max_suffix;
        } elif a == b {
            if k + 1 != period {
                # Keep scanning the equal strings
                k += 1;
            } else {
                # Matched a whole period. Start matching the next period.
                candidate += period;
                k = 0;
            }
        } else {
            # Did better than max_suffix, so replace it.
            max_suffix = candidate;
            candidate += 1;
            k = 0;
            period = 1;
        }
    }
    return (max_suffix, period);
}

"""_factorize: a critical factorization of the needle, the later of the two
maximal-suffix cuts (Crochemore and Perrin, 1991), as (cut, period of the
right half). Its local period is the needle's global period."""
def bl_factorize(needle: ptr[u8], len_needle: i64) -> tuple[i64, i64] {
    (cut1, period1) = bl_lex_search(needle, len_needle, False);
    (cut2, period2) = bl_lex_search(needle, len_needle, True);
    # Take the later cut.
    if cut1 > cut2 {
        return (cut1, period1);
    }
    return (cut2, period2);
}

"""_preprocess: fill the 64-entry compressed Boyer-Moore bad-character
`table` for the needle and return the rest of its prework as (cut, period,
gap, is_periodic)."""
def bl_preprocess(
    needle: ptr[u8], len_needle: i64, table: ptr[u8]
) -> tuple[i64, i64, i64, bool] {
    (cut, period) = bl_factorize(needle, len_needle);
    is_periodic = memcmp(ptr(needle), ptr(needle + period), u64(cut)) == i32(0);
    if not is_periodic {
        # A lower bound on the period
        period = imax(cut, len_needle - cut) + 1;
    }
    # The gap between the last character and the previous occurrence of an
    # equivalent character (modulo TABLE_SIZE)
    gap = len_needle;
    last = byte_at(needle, len_needle - 1) & TABLE_MASK;
    i = len_needle - 2;
    while i >= 0 {
        if (byte_at(needle, i) & TABLE_MASK) == last {
            gap = len_needle - 1 - i;
            break;
        }
        i -= 1;
    }
    # Fill up a compressed Boyer-Moore "Bad Character" table
    not_found_shift = imin(len_needle, MAX_SHIFT);
    for t in range(TABLE_SIZE) {
        set_byte(table, t, u8(not_found_shift));
    }
    for j in range(len_needle - not_found_shift, len_needle) {
        set_byte(table, i64(byte_at(needle, j) & TABLE_MASK), u8(len_needle - 1 - j));
    }
    return (cut, period, gap, is_periodic);
}

"""The bad-character shift of the byte `c`."""
def table_shift(table: ptr[u8], c: u8) -> i64 {
    return i64(byte_at(table, i64(c & TABLE_MASK)));
}

"""_two_way: Crochemore and Perrin's Two-Way search of the haystack for the
preprocessed needle, with Horspool skips from the shift table: the index of
the first match, or -1. The C's gotos become the `horspool` flag (false
for its `no_shift` re-entry) and `continue` (its window loop)."""
def bl_two_way(
    haystack: ptr[u8],
    len_haystack: i64,
    needle: ptr[u8],
    len_needle: i64,
    cut: i64,
    period_in: i64,
    gap: i64,
    is_periodic: bool,
    table: ptr[u8]
) -> i64 {
    period = period_in;
    # Indices into the haystack: window_last is C's window_last pointer.
    window_last: i64 = len_needle - 1;
    window: i64 = 0;
    shift: i64 = 0;
    i: i64 = 0;
    gap_jump_end = imin(len_needle, cut + gap);
    if is_periodic {
        memory: i64 = 0;
        horspool = True;
        while True {
            if horspool {
                if window_last >= len_haystack {
                    return -1;
                }
                while True {
                    shift = table_shift(table, byte_at(haystack, window_last));
                    window_last += shift;
                    if shift == 0 {
                        break;
                    }
                    if window_last >= len_haystack {
                        return -1;
                    }
                }
            }
            horspool = True;
            window = window_last - len_needle + 1;
            i = imax(cut, memory);
            right_matched = True;
            while i < len_needle {
                if byte_at(needle, i) != byte_at(haystack, window + i) {
                    if i < gap_jump_end {
                        # Early right half mismatch: jump by gap.
                        window_last += gap;
                    } else {
                        # Late right half mismatch: jump by n (>gap)
                        window_last += i - cut + 1;
                    }
                    memory = 0;
                    right_matched = False;
                    break;
                }
                i += 1;
            }
            if not right_matched {
                continue;
            }
            left_matched = True;
            i = memory;
            while i < cut {
                if byte_at(needle, i) != byte_at(haystack, window + i) {
                    # Left half does not match.
                    left_matched = False;
                    window_last += period;
                    memory = len_needle - period;
                    if window_last >= len_haystack {
                        return -1;
                    }
                    shift = table_shift(table, byte_at(haystack, window_last));
                    if shift != 0 {
                        # A mismatch has been identified to the right of
                        # where i will next start, so we can jump at least
                        # as far as if the mismatch occurred on the first
                        # comparison.
                        mem_jump = imax(cut, memory) - cut + 1;
                        memory = 0;
                        window_last += imax(shift, mem_jump);
                    } else {
                        horspool = False;
                    }
                    break;
                }
                i += 1;
            }
            if left_matched {
                return window;
            }
        }
    }
    period = imax(gap, period);
    while window_last < len_haystack {
        while True {
            shift = table_shift(table, byte_at(haystack, window_last));
            window_last += shift;
            if shift == 0 {
                break;
            }
            if window_last >= len_haystack {
                return -1;
            }
        }
        window = window_last - len_needle + 1;
        i = cut;
        right_matched = True;
        while i < len_needle {
            if byte_at(needle, i) != byte_at(haystack, window + i) {
                if i < gap_jump_end {
                    # Early right half mismatch: jump by gap.
                    window_last += gap;
                } else {
                    # Late right half mismatch: jump by n (>gap)
                    window_last += i - cut + 1;
                }
                right_matched = False;
                break;
            }
            i += 1;
        }
        if not right_matched {
            continue;
        }
        left_matched = True;
        i = 0;
        while i < cut {
            if byte_at(needle, i) != byte_at(haystack, window + i) {
                # Left half does not match.
                window_last += period;
                left_matched = False;
                break;
            }
            i += 1;
        }
        if left_matched {
            return window;
        }
    }
    return -1;
}

"""_two_way_find. The prework's shift table is on the heap (C keeps it on
the stack); without memory for it, the default search finds the same index."""
def bl_two_way_find(
    haystack: ptr[u8], len_haystack: i64, needle: ptr[u8], len_needle: i64
) -> i64 {
    table = ptr[u8](PyMem_Malloc(u64(TABLE_SIZE)));
    if not table {
        return bl_default_find(
            haystack, len_haystack, needle, len_needle, -1, BL_FAST_SEARCH
        );
    }
    (cut, period, gap, is_periodic) = bl_preprocess(needle, len_needle, table);
    result = bl_two_way(
        haystack, len_haystack, needle, len_needle, cut, period, gap, is_periodic, table
    );
    PyMem_Free(ptr(table));
    return result;
}

"""_two_way_count: up to `maxcount` non-overlapping matches."""
def bl_two_way_count(
    haystack: ptr[u8],
    len_haystack: i64,
    needle: ptr[u8],
    len_needle: i64,
    maxcount: i64
) -> i64 {
    table = ptr[u8](PyMem_Malloc(u64(TABLE_SIZE)));
    if not table {
        return bl_default_find(
            haystack, len_haystack, needle, len_needle, maxcount, BL_FAST_COUNT
        );
    }
    (cut, period, gap, is_periodic) = bl_preprocess(needle, len_needle, table);
    index: i64 = 0;
    count: i64 = 0;
    while True {
        result = bl_two_way(
            haystack + index,
            len_haystack - index,
            needle,
            len_needle,
            cut,
            period,
            gap,
            is_periodic,
            table
        );
        if result == -1 {
            break;
        }
        count += 1;
        if count == maxcount {
            break;
        }
        index += result + len_needle;
    }
    PyMem_Free(ptr(table));
    return count;
}

"""default_find: the bloom-filtered Horspool scan for a needle of at least
two bytes; the first index (FAST_SEARCH) or the match count (FAST_COUNT)."""
def bl_default_find(
    s: ptr[u8], n: i64, p: ptr[u8], m: i64, maxcount: i64, mode: i64
) -> i64 {
    w = n - m;
    mlast = m - 1;
    count: i64 = 0;
    gap = mlast;
    last = byte_at(p, mlast);
    ss = s + mlast;
    mask = u64(0);
    for k in range(mlast) {
        mask = bloom_add(mask, byte_at(p, k));
        if byte_at(p, k) == last {
            gap = mlast - k - 1;
        }
    }
    mask = bloom_add(mask, last);
    i: i64 = 0;
    j: i64 = 0;
    while i <= w {
        if byte_at(ss, i) == last {
            # candidate match
            j = 0;
            while j < mlast and byte_at(s, i + j) == byte_at(p, j) {
                j += 1;
            }
            if j == mlast {
                # got a match!
                if mode != BL_FAST_COUNT {
                    return i;
                }
                count += 1;
                if count == maxcount {
                    return maxcount;
                }
                i = i + mlast;
            } elif i + 1 <= w and not bloom(mask, byte_at(ss, i + 1)) {
                # miss: the next character is not part of the pattern
                i = i + m;
            } else {
                i = i + gap;
            }
        } elif i + 1 <= w and not bloom(mask, byte_at(ss, i + 1)) {
            # skip: the next character is not part of the pattern
            i = i + m;
        }
        i += 1;
    }
    return count if mode == BL_FAST_COUNT else -1;
}

"""adaptive_find: default_find that switches to the two-way search once it
has compared O(m) bytes without a match far from the haystack's end."""
def bl_adaptive_find(
    s: ptr[u8], n: i64, p: ptr[u8], m: i64, maxcount: i64, mode: i64
) -> i64 {
    w = n - m;
    mlast = m - 1;
    count: i64 = 0;
    gap = mlast;
    hits: i64 = 0;
    last = byte_at(p, mlast);
    ss = s + mlast;
    mask = u64(0);
    for k in range(mlast) {
        mask = bloom_add(mask, byte_at(p, k));
        if byte_at(p, k) == last {
            gap = mlast - k - 1;
        }
    }
    mask = bloom_add(mask, last);
    i: i64 = 0;
    j: i64 = 0;
    while i <= w {
        if byte_at(ss, i) == last {
            # candidate match
            j = 0;
            while j < mlast and byte_at(s, i + j) == byte_at(p, j) {
                j += 1;
            }
            if j == mlast {
                # got a match!
                if mode != BL_FAST_COUNT {
                    return i;
                }
                count += 1;
                if count == maxcount {
                    return maxcount;
                }
                i = i + mlast;
            } else {
                hits += j + 1;
                if hits > m // 4 and w - i > 2000 {
                    if mode == BL_FAST_SEARCH {
                        res = bl_two_way_find(s + i, n - i, p, m);
                        return -1 if res == -1 else res + i;
                    }
                    res = bl_two_way_count(s + i, n - i, p, m, maxcount - count);
                    return res + count;
                }
                # miss: check if next character is part of pattern
                if i + 1 <= w and not bloom(mask, byte_at(ss, i + 1)) {
                    i = i + m;
                } else {
                    i = i + gap;
                }
            }
        } elif i + 1 <= w and not bloom(mask, byte_at(ss, i + 1)) {
            # skip: check if next character is part of pattern
            i = i + m;
        }
        i += 1;
    }
    return count if mode == BL_FAST_COUNT else -1;
}

"""default_rfind: the last index of a needle of at least two bytes, or -1."""
def bl_default_rfind(
    s: ptr[u8], n: i64, p: ptr[u8], m: i64, maxcount: i64, mode: i64
) -> i64 {
    # create compressed boyer-moore delta 1 table
    mlast = m - 1;
    rskip = m - 1;
    w = n - m;
    first = byte_at(p, 0);
    # process pattern[0] outside the loop
    mask = bloom_add(u64(0), first);
    # process pattern[:0:-1]
    i = mlast;
    while i > 0 {
        mask = bloom_add(mask, byte_at(p, i));
        if byte_at(p, i) == first {
            rskip = i - 1;
        }
        i -= 1;
    }
    j: i64 = 0;
    i = w;
    while i >= 0 {
        if byte_at(s, i) == first {
            # candidate match
            j = mlast;
            while j > 0 and byte_at(s, i + j) == byte_at(p, j) {
                j -= 1;
            }
            if j == 0 {
                # got a match!
                return i;
            }
            # miss: check if previous character is part of pattern
            if i > 0 and not bloom(mask, byte_at(s, i - 1)) {
                i = i - m;
            } else {
                i = i - rskip;
            }
        } elif i > 0 and not bloom(mask, byte_at(s, i - 1)) {
            # skip: check if previous character is part of pattern
            i = i - m;
        }
        i -= 1;
    }
    return -1;
}

"""count_char: occurrences of `p0` in s[0:n], stopping at `maxcount`."""
def bl_count_char(s: ptr[u8], n: i64, p0: u8, maxcount: i64) -> i64 {
    count: i64 = 0;
    for i in range(n) {
        if byte_at(s, i) == p0 {
            count += 1;
            if count == maxcount {
                return maxcount;
            }
        }
    }
    return count;
}

"""count_char_no_maxcount: count_char without a cut-off."""
def bl_count_char_no_maxcount(s: ptr[u8], n: i64, p0: u8) -> i64 {
    count: i64 = 0;
    for i in range(n) {
        if byte_at(s, i) == p0 {
            count += 1;
        }
    }
    return count;
}

"""FASTSEARCH: search s[0:n] for p[0:m] by `mode`. FAST_SEARCH and
FAST_RSEARCH return the first or last index or -1; FAST_COUNT returns up to
`maxcount` non-overlapping matches, or -1 when no match is possible."""
def bl_fastsearch(
    s: ptr[u8], n: i64, p: ptr[u8], m: i64, maxcount: i64, mode: i64
) -> i64 {
    if n < m or (mode == BL_FAST_COUNT and maxcount == 0) {
        return -1;
    }
    # look for special cases
    if m <= 1 {
        if m <= 0 {
            return -1;
        }
        # use special case for 1-character strings
        if mode == BL_FAST_SEARCH {
            return bl_find_char(s, n, byte_at(p, 0));
        }
        if mode == BL_FAST_RSEARCH {
            return bl_rfind_char(s, n, byte_at(p, 0));
        }
        if maxcount == PY_SSIZE_T_MAX {
            return bl_count_char_no_maxcount(s, n, byte_at(p, 0));
        }
        return bl_count_char(s, n, byte_at(p, 0), maxcount);
    }
    if mode != BL_FAST_RSEARCH {
        if n < 2500 or (m < 100 and n < 30000) or m < 6 {
            return bl_default_find(s, n, p, m, maxcount, mode);
        }
        if (m >> 2) * 3 < (n >> 2) {
            # 33% threshold, but don't overflow. For larger problems where
            # the needle isn't a huge percentage of the size of the
            # haystack, the relatively expensive O(m) startup cost of the
            # two-way algorithm will surely pay off.
            if mode == BL_FAST_SEARCH {
                return bl_two_way_find(s, n, p, m);
            }
            return bl_two_way_count(s, n, p, m, maxcount);
        }
        # To ensure that we have good worst-case behavior, here's an
        # adaptive version of the algorithm, where if we match O(m)
        # characters without any matches of the entire needle, then we
        # predict that the startup cost of the two-way algorithm will
        # probably be worth it.
        return bl_adaptive_find(s, n, p, m, maxcount, mode);
    }
    return bl_default_rfind(s, n, p, m, maxcount, mode);
}

# stringlib/find.h and stringlib/count.h

"""stringlib_find: the first index of sub in s[0:str_len] plus `offset`,
or -1."""
def bl_find(s: ptr[u8], str_len: i64, sub: ptr[u8], sub_len: i64, offset: i64) -> i64 {
    if sub_len == 0 {
        return offset;
    }
    pos = bl_fastsearch(s, str_len, sub, sub_len, -1, BL_FAST_SEARCH);
    if pos >= 0 {
        pos += offset;
    }
    return pos;
}

"""stringlib_rfind: the last index of sub in s[0:str_len] plus `offset`,
or -1."""
def bl_rfind(s: ptr[u8], str_len: i64, sub: ptr[u8], sub_len: i64, offset: i64) -> i64 {
    if sub_len == 0 {
        return str_len + offset;
    }
    pos = bl_fastsearch(s, str_len, sub, sub_len, -1, BL_FAST_RSEARCH);
    if pos >= 0 {
        pos += offset;
    }
    return pos;
}

"""stringlib_find_slice: bl_find over s[start:end], as an index into s."""
def bl_find_slice(
    s: ptr[u8], str_len: i64, sub: ptr[u8], sub_len: i64, start: i64, end: i64
) -> i64 {
    return bl_find(s + start, end - start, sub, sub_len, start);
}

"""stringlib_rfind_slice: bl_rfind over s[start:end], as an index into s."""
def bl_rfind_slice(
    s: ptr[u8], str_len: i64, sub: ptr[u8], sub_len: i64, start: i64, end: i64
) -> i64 {
    return bl_rfind(s + start, end - start, sub, sub_len, start);
}

"""stringlib_count: non-overlapping matches of sub in s[0:str_len], at most
`maxcount`; an empty sub matches between every byte."""
def bl_count(
    s: ptr[u8], str_len: i64, sub: ptr[u8], sub_len: i64, maxcount: i64
) -> i64 {
    if str_len < 0 {
        # start > len(str)
        return 0;
    }
    if sub_len == 0 {
        return str_len + 1 if str_len < maxcount else maxcount;
    }
    count = bl_fastsearch(s, str_len, sub, sub_len, maxcount, BL_FAST_COUNT);
    if count < 0 {
        # no match
        return 0;
    }
    return count;
}

"""stringlib_find_max_char (find_max_char.h, one-byte): 255 when any byte
in [begin, stop) is non-ASCII, else 127. Aligned words are tested 8 bytes
at a time."""
def bl_find_max_char(begin: ptr[u8], stop: ptr[u8]) -> i64 {
    p = begin;
    while p < stop {
        if (int(p) & 7) == 0 {
            # Help register allocation
            q = p;
            while q + 8 <= stop {
                if (ptr[u64](q).view(1)[0] & UCS1_ASCII_CHAR_MASK) != u64(0) {
                    return 255;
                }
                q = q + 8;
            }
            p = q;
            if p == stop {
                break;
            }
        }
        if (p.view(1)[0] & u8(0x80)) != u8(0) {
            return 255;
        }
        p = p + 1;
    }
    return 127;
}

# Objects/bytes_methods.c

"""parse_args_finds_byte: the first argument of find, count and friends,
as (ok, buffer object, byte). A bytes-like argument comes back as the
buffer object; an integer in range(0, 256) comes back as the byte with a
NULL object."""
def parse_args_finds_byte(subobj: ptr[PyObject]) -> tuple[bool, ptr[PyObject], u8] {
    if PyObject_CheckBuffer(subobj) != i32(0) {
        return (True, subobj, u8(0));
    }
    if PyIndex_Check(subobj) == i32(0) {
        PyErr_Format(
            PyExc_TypeError,
            "argument should be integer or bytes-like object, not '%.200s'",
            object_type(subobj).view(1)[0].tp_name
        );
        return (False, NULL, u8(0));
    }
    ival = PyNumber_AsSsize_t(subobj, NULL);
    if ival == -1 and PyErr_Occurred() {
        return (False, NULL, u8(0));
    }
    if ival < 0 or ival > 255 {
        PyErr_SetString(PyExc_ValueError, "byte must be in range(0, 256)");
        return (False, NULL, u8(0));
    }
    return (True, NULL, u8(ival));
}

"""find_internal's search of s[start:end] (already adjusted) for sub, whose
first byte is `first`: forward when `direction` > 0, else backward."""
def find_in_range(
    s: ptr[u8],
    n: i64,
    sub: ptr[u8],
    sub_len: i64,
    first: u8,
    start: i64,
    end: i64,
    direction: i64
) -> i64 {
    if end - start < sub_len {
        return -1;
    }
    if sub_len == 1 {
        res = bl_find_char(s + start, end - start, first)
            if direction > 0
            else bl_rfind_char(s + start, end - start, first);
        if res >= 0 {
            res += start;
        }
        return res;
    }
    if direction > 0 {
        return bl_find_slice(s, n, sub, sub_len, start, end);
    }
    return bl_rfind_slice(s, n, sub, sub_len, start, end);
}

"""find_internal: the index of the argument in s[start:end], -1 when it is
absent, or -2 with an error set."""
def find_internal(
    s: ptr[u8],
    n: i64,
    subobj_in: ptr[PyObject],
    start_in: i64,
    end_in: i64,
    direction: i64
) -> i64 {
    (ok, subobj, byte) = parse_args_finds_byte(subobj_in);
    if not ok {
        return -2;
    }
    (start, end) = bl_adjust_indices(start_in, end_in, n);
    if not subobj {
        # sub is &byte, one byte long.
        return find_in_range(s, n, ptr[u8](), 1, byte, start, end, direction);
    }
    subbuf = new_buffer_slot();
    if not subbuf {
        return -2;
    }
    if PyObject_GetBuffer(subobj, subbuf, PyBUF_SIMPLE) != i32(0) {
        PyMem_Free(ptr(subbuf));
        return -2;
    }
    sub = ptr[u8](subbuf.view(1)[0].buf);
    sub_len = subbuf.view(1)[0].length;
    first = byte_at(sub, 0) if sub_len > 0 else u8(0);
    res = find_in_range(s, n, sub, sub_len, first, start, end, direction);
    release_buffer_slot(subbuf);
    return res;
}

"""stringlib_count of the single byte `ch`: the count path FASTSEARCH takes
for a one-byte needle and no limit."""
def count_byte(s: ptr[u8], n: i64, ch: u8) -> i64 {
    if n < 1 {
        return 0;
    }
    return bl_count_char_no_maxcount(s, n, ch);
}

"""tailmatch's comparison of s[start:end] (already adjusted) against sub:
at the start when `direction` < 0, else at the end."""
def tail_matches(
    s: ptr[u8], n: i64, sub: ptr[u8], slen: i64, start: i64, end: i64, direction: i64
) -> bool {
    lo = start;
    if direction < 0 {
        # startswith
        if lo > n - slen {
            return False;
        }
    } else {
        # endswith
        if end - lo < slen or lo > n {
            return False;
        }
        if end - slen > lo {
            lo = end - slen;
        }
    }
    if end - lo < slen {
        return False;
    }
    return memcmp(ptr(s + lo), ptr(sub), u64(slen)) == i32(0);
}

"""tailmatch: whether `substr` (bytes or bytes-like) matches the start
(`direction` < 0) or end of s[start:end]: 1 or 0, or -1 with an error set."""
def tailmatch(
    s: ptr[u8],
    n: i64,
    substr: ptr[PyObject],
    start_in: i64,
    end_in: i64,
    direction: i64
) -> i32 {
    view = ptr[Py_buffer]();
    sub = ptr[u8]();
    slen: i64 = 0;
    if type_has_feature(object_type(substr), Py_TPFLAGS_BYTES_SUBCLASS) {
        sub = PyBytes_AsString(substr);
        slen = object_size(substr);
    } else {
        view = new_buffer_slot();
        if not view {
            return i32(-1);
        }
        if PyObject_GetBuffer(substr, view, PyBUF_SIMPLE) != i32(0) {
            PyMem_Free(ptr(view));
            return i32(-1);
        }
        sub = ptr[u8](view.view(1)[0].buf);
        slen = view.view(1)[0].length;
    }
    (start, end) = bl_adjust_indices(start_in, end_in, n);
    found = tail_matches(s, n, sub, slen, start, end, direction);
    if view {
        release_buffer_slot(view);
    }
    return i32(1) if found else i32(0);
}

"""_Py_bytes_tailmatch: startswith and endswith over one prefix or suffix
or a tuple of them."""
def bytes_tailmatch(
    s: ptr[u8],
    n: i64,
    function_name: ptr[u8],
    subobj: ptr[PyObject],
    start: i64,
    end: i64,
    direction: i64
) -> ptr[PyObject] {
    if type_has_feature(object_type(subobj), Py_TPFLAGS_TUPLE_SUBCLASS) {
        for i in range(object_size(subobj)) {
            matched = tailmatch(s, n, tuple_get_item(subobj, i), start, end, direction);
            if matched < i32(0) {
                return NULL;
            }
            if matched != i32(0) {
                return PyBool_FromLong(1);
            }
        }
        return PyBool_FromLong(0);
    }
    result = tailmatch(s, n, subobj, start, end, direction);
    if result == i32(-1) {
        if PyErr_ExceptionMatches(PyExc_TypeError) != i32(0) {
            PyErr_Format(
                PyExc_TypeError,
                "%s first arg must be bytes or a tuple of bytes, not %s",
                function_name,
                object_type(subobj).view(1)[0].tp_name
            );
        }
        return NULL;
    }
    return PyBool_FromLong(i64(result));
}

import from c {
    def _Py_bytes_isspace(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        # Shortcut for single character strings
        if length == 1 and py_isspace(byte_at(cptr, 0)) {
            return PyBool_FromLong(1);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        for i in range(length) {
            if not py_isspace(byte_at(cptr, i)) {
                return PyBool_FromLong(0);
            }
        }
        return PyBool_FromLong(1);
    }  def _Py_bytes_isalpha(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        # Shortcut for single character strings
        if length == 1 and py_isalpha(byte_at(cptr, 0)) {
            return PyBool_FromLong(1);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        for i in range(length) {
            if not py_isalpha(byte_at(cptr, i)) {
                return PyBool_FromLong(0);
            }
        }
        return PyBool_FromLong(1);
    }  def _Py_bytes_isalnum(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        # Shortcut for single character strings
        if length == 1 and py_isalnum(byte_at(cptr, 0)) {
            return PyBool_FromLong(1);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        for i in range(length) {
            if not py_isalnum(byte_at(cptr, i)) {
                return PyBool_FromLong(0);
            }
        }
        return PyBool_FromLong(1);
    }  def _Py_bytes_isdigit(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        # Shortcut for single character strings
        if length == 1 and py_isdigit(byte_at(cptr, 0)) {
            return PyBool_FromLong(1);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        for i in range(length) {
            if not py_isdigit(byte_at(cptr, i)) {
                return PyBool_FromLong(0);
            }
        }
        return PyBool_FromLong(1);
    }  def _Py_bytes_islower(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        # Shortcut for single character strings
        if length == 1 {
            return PyBool_FromLong(1 if py_islower(byte_at(cptr, 0)) else 0);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        cased = False;
        for i in range(length) {
            c = byte_at(cptr, i);
            if py_isupper(c) {
                return PyBool_FromLong(0);
            } elif not cased and py_islower(c) {
                cased = True;
            }
        }
        return PyBool_FromLong(1 if cased else 0);
    }  def _Py_bytes_isupper(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        # Shortcut for single character strings
        if length == 1 {
            return PyBool_FromLong(1 if py_isupper(byte_at(cptr, 0)) else 0);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        cased = False;
        for i in range(length) {
            c = byte_at(cptr, i);
            if py_islower(c) {
                return PyBool_FromLong(0);
            } elif not cased and py_isupper(c) {
                cased = True;
            }
        }
        return PyBool_FromLong(1 if cased else 0);
    }  def _Py_bytes_istitle(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        if length == 1 {
            return PyBool_FromLong(1 if py_isupper(byte_at(cptr, 0)) else 0);
        }
        # Special case for empty strings
        if length == 0 {
            return PyBool_FromLong(0);
        }
        cased = False;
        previous_is_cased = False;
        for i in range(length) {
            c = byte_at(cptr, i);
            if py_isupper(c) {
                if previous_is_cased {
                    return PyBool_FromLong(0);
                }
                previous_is_cased = True;
                cased = True;
            } elif py_islower(c) {
                if not previous_is_cased {
                    return PyBool_FromLong(0);
                }
                previous_is_cased = True;
                cased = True;
            } else {
                previous_is_cased = False;
            }
        }
        return PyBool_FromLong(1 if cased else 0);
    }  def _Py_bytes_isascii(cptr: ptr[u8], length: i64) -> ptr[PyObject] {
        if bl_find_max_char(cptr, cptr + length) > 127 {
            return PyBool_FromLong(0);
        }
        return PyBool_FromLong(1);
    }
    # The case conversions store their `length` bytes in the preallocated
    # `result`.
    def _Py_bytes_lower(result: ptr[u8], cptr: ptr[u8], length: i64) {
        for i in range(length) {
            set_byte(result, i, py_tolower(byte_at(cptr, i)));
        }
    }  def _Py_bytes_upper(result: ptr[u8], cptr: ptr[u8], length: i64) {
        for i in range(length) {
            set_byte(result, i, py_toupper(byte_at(cptr, i)));
        }
    }  def _Py_bytes_title(result: ptr[u8], s: ptr[u8], length: i64) {
        previous_is_cased = False;
        for i in range(length) {
            c = byte_at(s, i);
            if py_islower(c) {
                if not previous_is_cased {
                    c = py_toupper(c);
                }
                previous_is_cased = True;
            } elif py_isupper(c) {
                if previous_is_cased {
                    c = py_tolower(c);
                }
                previous_is_cased = True;
            } else {
                previous_is_cased = False;
            }
            set_byte(result, i, c);
        }
    }  def _Py_bytes_capitalize(result: ptr[u8], s: ptr[u8], length: i64) {
        if length > 0 {
            set_byte(result, 0, py_toupper(byte_at(s, 0)));
            _Py_bytes_lower(result + 1, s + 1, length - 1);
        }
    }  def _Py_bytes_swapcase(result: ptr[u8], s: ptr[u8], length: i64) {
        for i in range(length) {
            c = byte_at(s, i);
            if py_islower(c) {
                set_byte(result, i, py_toupper(c));
            } elif py_isupper(c) {
                set_byte(result, i, py_tolower(c));
            } else {
                set_byte(result, i, c);
            }
        }
    }  def _Py_bytes_maketrans(
        frm: ptr[Py_buffer], to_buf: ptr[Py_buffer]
    ) -> ptr[PyObject] {
        if frm.view(1)[0].length != to_buf.view(1)[0].length {
            PyErr_Format(PyExc_ValueError, "maketrans arguments must have same length");
            return NULL;
        }
        res = PyBytes_FromStringAndSize(ptr[u8](), 256);
        if not res {
            return NULL;
        }
        p = PyBytes_AsString(res);
        for i in range(256) {
            set_byte(p, i, u8(i));
        }
        source = ptr[u8](frm.view(1)[0].buf);
        target = ptr[u8](to_buf.view(1)[0].buf);
        for k in range(frm.view(1)[0].length) {
            set_byte(p, i64(byte_at(source, k)), byte_at(target, k));
        }
        return res;
    }  def _Py_bytes_find(
        s: ptr[u8], length: i64, sub: ptr[PyObject], start: i64, end: i64
    ) -> ptr[PyObject] {
        result = find_internal(s, length, sub, start, end, 1);
        if result == -2 {
            return NULL;
        }
        return PyLong_FromSsize_t(result);
    }  def _Py_bytes_index(
        s: ptr[u8], length: i64, sub: ptr[PyObject], start: i64, end: i64
    ) -> ptr[PyObject] {
        result = find_internal(s, length, sub, start, end, 1);
        if result == -2 {
            return NULL;
        }
        if result == -1 {
            PyErr_SetString(PyExc_ValueError, "subsection not found");
            return NULL;
        }
        return PyLong_FromSsize_t(result);
    }  def _Py_bytes_rfind(
        s: ptr[u8], length: i64, sub: ptr[PyObject], start: i64, end: i64
    ) -> ptr[PyObject] {
        result = find_internal(s, length, sub, start, end, -1);
        if result == -2 {
            return NULL;
        }
        return PyLong_FromSsize_t(result);
    }  def _Py_bytes_rindex(
        s: ptr[u8], length: i64, sub: ptr[PyObject], start: i64, end: i64
    ) -> ptr[PyObject] {
        result = find_internal(s, length, sub, start, end, -1);
        if result == -2 {
            return NULL;
        }
        if result == -1 {
            PyErr_SetString(PyExc_ValueError, "subsection not found");
            return NULL;
        }
        return PyLong_FromSsize_t(result);
    }  def _Py_bytes_count(
        s: ptr[u8], length: i64, sub_obj_in: ptr[PyObject], start_in: i64, end_in: i64
    ) -> ptr[PyObject] {
        (ok, sub_obj, byte) = parse_args_finds_byte(sub_obj_in);
        if not ok {
            return NULL;
        }
        (start, end) = bl_adjust_indices(start_in, end_in, length);
        if not sub_obj {
            # sub is &byte, one byte long.
            return PyLong_FromSsize_t(count_byte(s + start, end - start, byte));
        }
        vsub = new_buffer_slot();
        if not vsub {
            return NULL;
        }
        if PyObject_GetBuffer(sub_obj, vsub, PyBUF_SIMPLE) != i32(0) {
            PyMem_Free(ptr(vsub));
            return NULL;
        }
        count_obj = PyLong_FromSsize_t(
            bl_count(
                s + start,
                end - start,
                ptr[u8](vsub.view(1)[0].buf),
                vsub.view(1)[0].length,
                PY_SSIZE_T_MAX
            )
        );
        release_buffer_slot(vsub);
        return count_obj;
    }  def _Py_bytes_contains(s: ptr[u8], length: i64, arg: ptr[PyObject]) -> i32 {
        ival = PyNumber_AsSsize_t(arg, NULL);
        if ival == -1 and PyErr_Occurred() {
            PyErr_Clear();
            varg = new_buffer_slot();
            if not varg {
                return i32(-1);
            }
            if PyObject_GetBuffer(arg, varg, PyBUF_SIMPLE) != i32(0) {
                PyMem_Free(ptr(varg));
                return i32(-1);
            }
            pos = bl_find(
                s, length, ptr[u8](varg.view(1)[0].buf), varg.view(1)[0].length, 0
            );
            release_buffer_slot(varg);
            return i32(1) if pos >= 0 else i32(0);
        }
        if ival < 0 or ival >= 256 {
            PyErr_SetString(PyExc_ValueError, "byte must be in range(0, 256)");
            return i32(-1);
        }
        if memchr(ptr(s), i32(ival), u64(length)).is_null() {
            return i32(0);
        }
        return i32(1);
    }  def _Py_bytes_startswith(
        s: ptr[u8], length: i64, subobj: ptr[PyObject], start: i64, end: i64
    ) -> ptr[PyObject] {
        return bytes_tailmatch(
            s, length, ptr[u8]("startswith"), subobj, start, end, -1
        );
    }  def _Py_bytes_endswith(
        s: ptr[u8], length: i64, subobj: ptr[PyObject], start: i64, end: i64
    ) -> ptr[PyObject] {
        return bytes_tailmatch(s, length, ptr[u8]("endswith"), subobj, start, end, 1);
    }
}

# stringlib/split.h

"""PREALLOC_SIZE: list slots to preallocate for at most `maxsplit` splits."""
def prealloc_size(maxsplit: i64) -> i64 {
    return MAX_PREALLOC if maxsplit >= MAX_PREALLOC else maxsplit + 1;
}

"""PyList_SET_ITEM: store `item` (stealing it) in an empty slot."""
def list_set_item(parts: ptr[PyObject], index: i64, item: ptr[PyObject]) {
    (fast_items(parts) + index).view(1)[0] = item;
}

"""FIX_PREALLOC_SIZE: Py_SET_SIZE(list, count)."""
def fix_prealloc_size(parts: ptr[PyObject], count: i64) {
    ptr[PyVarObject](parts).view(1)[0].ob_size = count;
}

"""SPLIT_ADD: data[left:right] as item `count` of `parts`, stored in a
preallocated slot while they last and appended after; False on error."""
def split_add(
    mutable: bool,
    parts: ptr[PyObject],
    count: i64,
    data: ptr[u8],
    left: i64,
    right: i64
) -> bool {
    sub = bl_new(mutable, data + left, right - left);
    if not sub {
        return False;
    }
    if count < MAX_PREALLOC {
        list_set_item(parts, count, sub);
        return True;
    }
    if PyList_Append(parts, sub) != i32(0) {
        object_decref(sub);
        return False;
    }
    object_decref(sub);
    return True;
}

"""SPLIT_APPEND: append data[left:right] to `parts`; False on error."""
def split_append(
    mutable: bool, parts: ptr[PyObject], data: ptr[u8], left: i64, right: i64
) -> bool {
    sub = bl_new(mutable, data + left, right - left);
    if not sub {
        return False;
    }
    if PyList_Append(parts, sub) != i32(0) {
        object_decref(sub);
        return False;
    }
    object_decref(sub);
    return True;
}

"""The onError exit of split.h: drop the partial list."""
def split_failed(parts: ptr[PyObject]) -> ptr[PyObject] {
    object_decref(parts);
    return NULL;
}

"""stringlib_split_whitespace: split(None, maxcount) of `str_obj`'s bytes
s[0:str_len]."""
def bl_split_whitespace(
    str_obj: ptr[PyObject], s: ptr[u8], str_len: i64, maxcount_in: i64
) -> ptr[PyObject] {
    mutable = bl_mutable(str_obj);
    maxcount = maxcount_in;
    count: i64 = 0;
    parts = PyList_New(prealloc_size(maxcount));
    if not parts {
        return NULL;
    }
    i: i64 = 0;
    j: i64 = 0;
    while maxcount > 0 {
        maxcount -= 1;
        while i < str_len and py_isspace(byte_at(s, i)) {
            i += 1;
        }
        if i == str_len {
            break;
        }
        j = i;
        i += 1;
        while i < str_len and not py_isspace(byte_at(s, i)) {
            i += 1;
        }
        if not mutable and j == 0 and i == str_len and bytes_check_exact(str_obj) {
            # No whitespace in str_obj, so just use it as list[0]
            list_set_item(parts, 0, object_new_ref(str_obj));
            count += 1;
            break;
        }
        if not split_add(mutable, parts, count, s, j, i) {
            return split_failed(parts);
        }
        count += 1;
    }
    if i < str_len {
        # Only occurs when maxcount was reached. Skip any remaining
        # whitespace and copy to end of string
        while i < str_len and py_isspace(byte_at(s, i)) {
            i += 1;
        }
        if i != str_len {
            if not split_add(mutable, parts, count, s, i, str_len) {
                return split_failed(parts);
            }
            count += 1;
        }
    }
    fix_prealloc_size(parts, count);
    return parts;
}

"""stringlib_split_char: split by the one-byte separator `ch`."""
def bl_split_char(
    str_obj: ptr[PyObject], s: ptr[u8], str_len: i64, ch: u8, maxcount_in: i64
) -> ptr[PyObject] {
    mutable = bl_mutable(str_obj);
    maxcount = maxcount_in;
    count: i64 = 0;
    parts = PyList_New(prealloc_size(maxcount));
    if not parts {
        return NULL;
    }
    i: i64 = 0;
    j: i64 = 0;
    while j < str_len and maxcount > 0 {
        maxcount -= 1;
        while j < str_len {
            # I found that using memchr makes no difference
            if byte_at(s, j) == ch {
                if not split_add(mutable, parts, count, s, i, j) {
                    return split_failed(parts);
                }
                count += 1;
                j = j + 1;
                i = j;
                break;
            }
            j += 1;
        }
    }
    if not mutable and count == 0 and bytes_check_exact(str_obj) {
        # ch not in str_obj, so just use str_obj as list[0]
        list_set_item(parts, 0, object_new_ref(str_obj));
        count += 1;
    } elif i <= str_len {
        if not split_add(mutable, parts, count, s, i, str_len) {
            return split_failed(parts);
        }
        count += 1;
    }
    fix_prealloc_size(parts, count);
    return parts;
}

"""stringlib_split: split by the separator sep[0:sep_len]."""
def bl_split(
    str_obj: ptr[PyObject],
    s: ptr[u8],
    str_len: i64,
    sep: ptr[u8],
    sep_len: i64,
    maxcount_in: i64
) -> ptr[PyObject] {
    if sep_len == 0 {
        PyErr_SetString(PyExc_ValueError, "empty separator");
        return NULL;
    }
    if sep_len == 1 {
        return bl_split_char(str_obj, s, str_len, byte_at(sep, 0), maxcount_in);
    }
    mutable = bl_mutable(str_obj);
    maxcount = maxcount_in;
    count: i64 = 0;
    parts = PyList_New(prealloc_size(maxcount));
    if not parts {
        return NULL;
    }
    i: i64 = 0;
    j: i64 = 0;
    while maxcount > 0 {
        maxcount -= 1;
        pos = bl_fastsearch(s + i, str_len - i, sep, sep_len, -1, BL_FAST_SEARCH);
        if pos < 0 {
            break;
        }
        j = i + pos;
        if not split_add(mutable, parts, count, s, i, j) {
            return split_failed(parts);
        }
        count += 1;
        i = j + sep_len;
    }
    if not mutable and count == 0 and bytes_check_exact(str_obj) {
        # No match in str_obj, so just use it as list[0]
        list_set_item(parts, 0, object_new_ref(str_obj));
        count += 1;
    } else {
        if not split_add(mutable, parts, count, s, i, str_len) {
            return split_failed(parts);
        }
        count += 1;
    }
    fix_prealloc_size(parts, count);
    return parts;
}

"""stringlib_rsplit_whitespace: rsplit(None, maxcount)."""
def bl_rsplit_whitespace(
    str_obj: ptr[PyObject], s: ptr[u8], str_len: i64, maxcount_in: i64
) -> ptr[PyObject] {
    mutable = bl_mutable(str_obj);
    maxcount = maxcount_in;
    count: i64 = 0;
    parts = PyList_New(prealloc_size(maxcount));
    if not parts {
        return NULL;
    }
    i = str_len - 1;
    j = str_len - 1;
    while maxcount > 0 {
        maxcount -= 1;
        while i >= 0 and py_isspace(byte_at(s, i)) {
            i -= 1;
        }
        if i < 0 {
            break;
        }
        j = i;
        i -= 1;
        while i >= 0 and not py_isspace(byte_at(s, i)) {
            i -= 1;
        }
        if not mutable and j == str_len - 1 and i < 0 and bytes_check_exact(str_obj) {
            # No whitespace in str_obj, so just use it as list[0]
            list_set_item(parts, 0, object_new_ref(str_obj));
            count += 1;
            break;
        }
        if not split_add(mutable, parts, count, s, i + 1, j + 1) {
            return split_failed(parts);
        }
        count += 1;
    }
    if i >= 0 {
        # Only occurs when maxcount was reached. Skip any remaining
        # whitespace and copy to beginning of string
        while i >= 0 and py_isspace(byte_at(s, i)) {
            i -= 1;
        }
        if i >= 0 {
            if not split_add(mutable, parts, count, s, 0, i + 1) {
                return split_failed(parts);
            }
            count += 1;
        }
    }
    fix_prealloc_size(parts, count);
    if PyList_Reverse(parts) < i32(0) {
        return split_failed(parts);
    }
    return parts;
}

"""stringlib_rsplit_char: rsplit by the one-byte separator `ch`."""
def bl_rsplit_char(
    str_obj: ptr[PyObject], s: ptr[u8], str_len: i64, ch: u8, maxcount_in: i64
) -> ptr[PyObject] {
    mutable = bl_mutable(str_obj);
    maxcount = maxcount_in;
    count: i64 = 0;
    parts = PyList_New(prealloc_size(maxcount));
    if not parts {
        return NULL;
    }
    i = str_len - 1;
    j = str_len - 1;
    while i >= 0 and maxcount > 0 {
        maxcount -= 1;
        while i >= 0 {
            if byte_at(s, i) == ch {
                if not split_add(mutable, parts, count, s, i + 1, j + 1) {
                    return split_failed(parts);
                }
                count += 1;
                j = i - 1;
                i = j;
                break;
            }
            i -= 1;
        }
    }
    if not mutable and count == 0 and bytes_check_exact(str_obj) {
        # ch not in str_obj, so just use str_obj as list[0]
        list_set_item(parts, 0, object_new_ref(str_obj));
        count += 1;
    } elif j >= -1 {
        if not split_add(mutable, parts, count, s, 0, j + 1) {
            return split_failed(parts);
        }
        count += 1;
    }
    fix_prealloc_size(parts, count);
    if PyList_Reverse(parts) < i32(0) {
        return split_failed(parts);
    }
    return parts;
}

"""stringlib_rsplit: rsplit by the separator sep[0:sep_len]."""
def bl_rsplit(
    str_obj: ptr[PyObject],
    s: ptr[u8],
    str_len: i64,
    sep: ptr[u8],
    sep_len: i64,
    maxcount_in: i64
) -> ptr[PyObject] {
    if sep_len == 0 {
        PyErr_SetString(PyExc_ValueError, "empty separator");
        return NULL;
    }
    if sep_len == 1 {
        return bl_rsplit_char(str_obj, s, str_len, byte_at(sep, 0), maxcount_in);
    }
    mutable = bl_mutable(str_obj);
    maxcount = maxcount_in;
    count: i64 = 0;
    parts = PyList_New(prealloc_size(maxcount));
    if not parts {
        return NULL;
    }
    j = str_len;
    while maxcount > 0 {
        maxcount -= 1;
        pos = bl_fastsearch(s, j, sep, sep_len, -1, BL_FAST_RSEARCH);
        if pos < 0 {
            break;
        }
        if not split_add(mutable, parts, count, s, pos + sep_len, j) {
            return split_failed(parts);
        }
        count += 1;
        j = pos;
    }
    if not mutable and count == 0 and bytes_check_exact(str_obj) {
        # No match in str_obj, so just use it as list[0]
        list_set_item(parts, 0, object_new_ref(str_obj));
        count += 1;
    } else {
        if not split_add(mutable, parts, count, s, 0, j) {
            return split_failed(parts);
        }
        count += 1;
    }
    fix_prealloc_size(parts, count);
    if PyList_Reverse(parts) < i32(0) {
        return split_failed(parts);
    }
    return parts;
}

"""stringlib_splitlines: split at \\n, \\r and \\r\\n, keeping the line
breaks when `keepends` is nonzero. The list is not preallocated (it usually
gets hundreds of lines)."""
def bl_splitlines(
    str_obj: ptr[PyObject], s: ptr[u8], str_len: i64, keepends: i32
) -> ptr[PyObject] {
    mutable = bl_mutable(str_obj);
    parts = PyList_New(0);
    if not parts {
        return NULL;
    }
    i: i64 = 0;
    j: i64 = 0;
    while i < str_len {
        # Find a line and append it
        while i < str_len and not is_linebreak(byte_at(s, i)) {
            i += 1;
        }
        # Skip the line break reading CRLF as one line break
        eol = i;
        if i < str_len {
            if byte_at(s, i) == CHAR_RETURN
                and i + 1 < str_len
                and byte_at(s, i + 1) == CHAR_NEWLINE {
                i += 2;
            } else {
                i += 1;
            }
            if keepends != i32(0) {
                eol = i;
            }
        }
        if not mutable and j == 0 and eol == str_len and bytes_check_exact(str_obj) {
            # No linebreak in str_obj, so just use it as list[0]
            if PyList_Append(parts, str_obj) != i32(0) {
                return split_failed(parts);
            }
            break;
        }
        if not split_append(mutable, parts, s, j, eol) {
            return split_failed(parts);
        }
        j = i;
    }
    return parts;
}

# stringlib/partition.h

"""The three parts of a partition: str[0:pos], sep_obj and the rest after
the separator."""
def partition_found(
    mutable: bool,
    out: ptr[PyObject],
    s: ptr[u8],
    str_len: i64,
    sep_obj: ptr[PyObject],
    sep_len: i64,
    pos: i64
) -> ptr[PyObject] {
    tuple_set_item(out, 0, bl_new(mutable, s, pos));
    tuple_set_item(out, 1, object_new_ref(sep_obj));
    after = pos + sep_len;
    tuple_set_item(out, 2, bl_new(mutable, s + after, str_len - after));
    if PyErr_Occurred() {
        object_decref(out);
        return NULL;
    }
    return out;
}

"""stringlib_partition: (head, sep, tail) around the first sep, or
(str, empty, empty)."""
def bl_partition(
    str_obj: ptr[PyObject],
    s: ptr[u8],
    str_len: i64,
    sep_obj: ptr[PyObject],
    sep: ptr[u8],
    sep_len: i64
) -> ptr[PyObject] {
    if sep_len == 0 {
        PyErr_SetString(PyExc_ValueError, "empty separator");
        return NULL;
    }
    out = PyTuple_New(3);
    if not out {
        return NULL;
    }
    mutable = bl_mutable(str_obj);
    pos = bl_fastsearch(s, str_len, sep, sep_len, -1, BL_FAST_SEARCH);
    if pos < 0 {
        if mutable {
            tuple_set_item(out, 0, bl_new(True, s, str_len));
            tuple_set_item(out, 1, bl_new(True, ptr[u8](), 0));
            tuple_set_item(out, 2, bl_new(True, ptr[u8](), 0));
            if PyErr_Occurred() {
                object_decref(out);
                return NULL;
            }
        } else {
            tuple_set_item(out, 0, object_new_ref(str_obj));
            tuple_set_item(out, 1, bytes_get_empty());
            tuple_set_item(out, 2, bytes_get_empty());
        }
        return out;
    }
    return partition_found(mutable, out, s, str_len, sep_obj, sep_len, pos);
}

"""stringlib_rpartition: (head, sep, tail) around the last sep, or
(empty, empty, str)."""
def bl_rpartition(
    str_obj: ptr[PyObject],
    s: ptr[u8],
    str_len: i64,
    sep_obj: ptr[PyObject],
    sep: ptr[u8],
    sep_len: i64
) -> ptr[PyObject] {
    if sep_len == 0 {
        PyErr_SetString(PyExc_ValueError, "empty separator");
        return NULL;
    }
    out = PyTuple_New(3);
    if not out {
        return NULL;
    }
    mutable = bl_mutable(str_obj);
    pos = bl_fastsearch(s, str_len, sep, sep_len, -1, BL_FAST_RSEARCH);
    if pos < 0 {
        if mutable {
            tuple_set_item(out, 0, bl_new(True, ptr[u8](), 0));
            tuple_set_item(out, 1, bl_new(True, ptr[u8](), 0));
            tuple_set_item(out, 2, bl_new(True, s, str_len));
            if PyErr_Occurred() {
                object_decref(out);
                return NULL;
            }
        } else {
            tuple_set_item(out, 0, bytes_get_empty());
            tuple_set_item(out, 1, bytes_get_empty());
            tuple_set_item(out, 2, object_new_ref(str_obj));
        }
        return out;
    }
    return partition_found(mutable, out, s, str_len, sep_obj, sep_len, pos);
}

# stringlib/join.h

"""stringlib_bytes_join: the items of `iterable` (bytes-like) joined by
`sep`, a bytes or bytearray like `sep`. The Py_buffer array is always on
the heap (C uses ten on the stack for short sequences)."""
def bl_bytes_join(sep: ptr[PyObject], iterable: ptr[PyObject]) -> ptr[PyObject] {
    mutable = bl_mutable(sep);
    sepstr = bl_str(sep);
    seplen = bl_len(sep);
    seq = PySequence_Fast(iterable, "can only join an iterable");
    if not seq {
        return NULL;
    }
    seqlen = object_size(seq);
    if seqlen == 0 {
        object_decref(seq);
        return bl_new(mutable, ptr[u8](), 0);
    }
    if not mutable and seqlen == 1 {
        item = fast_items(seq).view(1)[0];
        if bytes_check_exact(item) {
            object_incref(item);
            object_decref(seq);
            return item;
        }
    }
    buffers = ptr[u8](PyMem_Calloc(u64(seqlen), u64(PY_BUFFER_SIZE)));
    if not buffers {
        object_decref(seq);
        PyErr_NoMemory();
        return NULL;
    }
    # Here is the general case. Do a pre-pass to figure out the total amount
    # of space we'll need (sz), and see whether all arguments are bytes-like.
    sz: i64 = 0;
    nbufs: i64 = 0;
    drop_gil = True;
    failed = False;
    i: i64 = 0;
    while i < seqlen {
        item = (fast_items(seq) + i).view(1)[0];
        view = buffer_at(buffers, i);
        if bytes_check_exact(item) {
            # Fast path.
            view.view(1)[0].owner = object_new_ref(item);
            view.view(1)[0].buf = ptr(PyBytes_AsString(item));
            view.view(1)[0].length = object_size(item);
        } else {
            if PyObject_GetBuffer(item, view, PyBUF_SIMPLE) != i32(0) {
                PyErr_Format(
                    PyExc_TypeError,
                    "sequence item %zd: expected a bytes-like object, %.80s found",
                    i,
                    object_type(item).view(1)[0].tp_name
                );
                failed = True;
                break;
            }
            # If the backing objects are mutable, then dropping the GIL
            # opens up race conditions where another thread tries to modify
            # the object which we hold a buffer on it. Such code has data
            # races anyway, but this is a conservative approach that avoids
            # changing the behaviour of that data race.
            drop_gil = False;
        }
        # for error cleanup
        nbufs = i + 1;
        itemlen = view.view(1)[0].length;
        if itemlen > PY_SSIZE_T_MAX - sz {
            PyErr_SetString(PyExc_OverflowError, "join() result is too long");
            failed = True;
            break;
        }
        sz += itemlen;
        if i != 0 {
            if seplen > PY_SSIZE_T_MAX - sz {
                PyErr_SetString(PyExc_OverflowError, "join() result is too long");
                failed = True;
                break;
            }
            sz += seplen;
        }
        if seqlen != object_size(seq) {
            PyErr_SetString(
                PyExc_RuntimeError, "sequence changed size during iteration"
            );
            failed = True;
            break;
        }
        i += 1;
    }
    res = NULL;
    if not failed {
        # Allocate result space.
        res = bl_new(mutable, ptr[u8](), sz);
    }
    if res {
        # Catenate everything.
        p = bl_str(res);
        if sz < GIL_THRESHOLD {
            # Benefits are likely outweighed by the overheads
            drop_gil = False;
        }
        save = ptr[PyThreadState]();
        if drop_gil {
            save = PyEval_SaveThread();
        }
        if seplen == 0 {
            # fast path
            for k in range(nbufs) {
                view = buffer_at(buffers, k);
                n = view.view(1)[0].length;
                memcpy(ptr(p), view.view(1)[0].buf, u64(n));
                p = p + n;
            }
        } else {
            for k in range(nbufs) {
                if k != 0 {
                    memcpy(ptr(p), ptr(sepstr), u64(seplen));
                    p = p + seplen;
                }
                view = buffer_at(buffers, k);
                n = view.view(1)[0].length;
                memcpy(ptr(p), view.view(1)[0].buf, u64(n));
                p = p + n;
            }
        }
        if drop_gil {
            PyEval_RestoreThread(save);
        }
    }
    object_decref(seq);
    for k in range(nbufs) {
        PyBuffer_Release(buffer_at(buffers, k));
    }
    PyMem_Free(ptr(buffers));
    return res;
}

# stringlib/ctype.h: METH_NOARGS methods over the shared functions.

def bl_isspace(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_isspace(bl_str(op), bl_len(op));
}

def bl_isalpha(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_isalpha(bl_str(op), bl_len(op));
}

def bl_isalnum(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_isalnum(bl_str(op), bl_len(op));
}

def bl_isascii(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_isascii(bl_str(op), bl_len(op));
}

def bl_isdigit(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_isdigit(bl_str(op), bl_len(op));
}

def bl_islower(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_islower(bl_str(op), bl_len(op));
}

def bl_isupper(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_isupper(bl_str(op), bl_len(op));
}

def bl_istitle(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return _Py_bytes_istitle(bl_str(op), bl_len(op));
}

"""A new object like `op` and as long, uninitialized, for a case
conversion to fill."""
def new_like(op: ptr[PyObject]) -> ptr[PyObject] {
    return bl_new(bl_mutable(op), ptr[u8](), bl_len(op));
}

def bl_lower(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    newobj = new_like(op);
    if not newobj {
        return NULL;
    }
    _Py_bytes_lower(bl_str(newobj), bl_str(op), bl_len(op));
    return newobj;
}

def bl_upper(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    newobj = new_like(op);
    if not newobj {
        return NULL;
    }
    _Py_bytes_upper(bl_str(newobj), bl_str(op), bl_len(op));
    return newobj;
}

def bl_title(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    newobj = new_like(op);
    if not newobj {
        return NULL;
    }
    _Py_bytes_title(bl_str(newobj), bl_str(op), bl_len(op));
    return newobj;
}

def bl_capitalize(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    newobj = new_like(op);
    if not newobj {
        return NULL;
    }
    _Py_bytes_capitalize(bl_str(newobj), bl_str(op), bl_len(op));
    return newobj;
}

def bl_swapcase(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    newobj = new_like(op);
    if not newobj {
        return NULL;
    }
    _Py_bytes_swapcase(bl_str(newobj), bl_str(op), bl_len(op));
    return newobj;
}

# stringlib/transmogrify.h

"""return_self: `op` itself when it is exactly bytes, else a new copy of
its bytes."""
def bl_return_self(op: ptr[PyObject]) -> ptr[PyObject] {
    mutable = bl_mutable(op);
    if not mutable and bytes_check_exact(op) {
        return object_new_ref(op);
    }
    return bl_new(mutable, bl_str(op), bl_len(op));
}

def expandtabs_overflow -> ptr[PyObject] {
    PyErr_SetString(PyExc_OverflowError, "result too long");
    return NULL;
}

"""stringlib_expandtabs_impl: a copy with every tab expanded to spaces up
to the next multiple of `tabsize` columns."""
def bl_expandtabs_impl(op: ptr[PyObject], tabsize: i32) -> ptr[PyObject] {
    s = bl_str(op);
    n = bl_len(op);
    tab = i64(tabsize);
    # First pass: determine size of output string
    i: i64 = 0;
    j: i64 = 0;
    p: i64 = 0;
    while p < n {
        c = byte_at(s, p);
        if c == CHAR_TAB {
            if tab > 0 {
                incr = tab - (j % tab);
                if j > PY_SSIZE_T_MAX - incr {
                    return expandtabs_overflow();
                }
                j += incr;
            }
        } else {
            if j > PY_SSIZE_T_MAX - 1 {
                return expandtabs_overflow();
            }
            j += 1;
            if c == CHAR_NEWLINE or c == CHAR_RETURN {
                if i > PY_SSIZE_T_MAX - j {
                    return expandtabs_overflow();
                }
                i += j;
                j = 0;
            }
        }
        p += 1;
    }
    if i > PY_SSIZE_T_MAX - j {
        return expandtabs_overflow();
    }
    # Second pass: create output string and fill it
    u = bl_new(bl_mutable(op), ptr[u8](), i + j);
    if not u {
        return NULL;
    }
    j = 0;
    q = bl_str(u);
    p = 0;
    while p < n {
        c = byte_at(s, p);
        if c == CHAR_TAB {
            if tab > 0 {
                fill = tab - (j % tab);
                j += fill;
                memset(ptr(q), i32(CHAR_SPACE), u64(fill));
                q = q + fill;
            }
        } else {
            j += 1;
            q.view(1)[0] = c;
            q = q + 1;
            if c == CHAR_NEWLINE or c == CHAR_RETURN {
                j = 0;
            }
        }
        p += 1;
    }
    return u;
}

"""expandtabs(tabsize) with the argument still an object."""
def expandtabs_with(op: ptr[PyObject], value: ptr[PyObject]) -> ptr[PyObject] {
    tabsize = PyLong_AsInt(value);
    if tabsize == i32(-1) and PyErr_Occurred() {
        return NULL;
    }
    return bl_expandtabs_impl(op, tabsize);
}

def expandtabs_bound(args: BoundArguments) -> ptr[PyObject] {
    if not args.values[0] {
        return bl_expandtabs_impl(args.context, i32(8));
    }
    return expandtabs_with(args.context, args.values[0]);
}

"""stringlib_expandtabs (METH_FASTCALL | METH_KEYWORDS): expandtabs($self,
/, tabsize=8). Positional calls are parsed inline, keywords through the
shared parser."""
def bl_expandtabs(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs == 0 {
        return bl_expandtabs_impl(op, i32(8));
    }
    if not kwnames and nargs == 1 {
        return expandtabs_with(op, args.view(1)[0]);
    }
    return invoke_vector(
        expandtabs_signature, args, nargs, kwnames, expandtabs_bound, op
    );
}

"""pad: a copy of `op` with `left` and `right` fill bytes around it (a
negative count is none), or `op` per return_self when both are 0."""
def bl_pad(op: ptr[PyObject], left_in: i64, right_in: i64, fill: u8) -> ptr[PyObject] {
    left = imax(left_in, 0);
    right = imax(right_in, 0);
    if left == 0 and right == 0 {
        return bl_return_self(op);
    }
    n = bl_len(op);
    u = bl_new(bl_mutable(op), ptr[u8](), left + n + right);
    if u {
        p = bl_str(u);
        if left != 0 {
            memset(ptr(p), i32(fill), u64(left));
        }
        memcpy(ptr(p + left), ptr(bl_str(op)), u64(n));
        if right != 0 {
            memset(ptr(p + left + n), i32(fill), u64(right));
        }
    }
    return u;
}

"""stringlib_ljust_impl."""
def bl_ljust_impl(op: ptr[PyObject], width: i64, fillchar: u8) -> ptr[PyObject] {
    if bl_len(op) >= width {
        return bl_return_self(op);
    }
    return bl_pad(op, 0, width - bl_len(op), fillchar);
}

"""stringlib_rjust_impl."""
def bl_rjust_impl(op: ptr[PyObject], width: i64, fillchar: u8) -> ptr[PyObject] {
    if bl_len(op) >= width {
        return bl_return_self(op);
    }
    return bl_pad(op, width - bl_len(op), 0, fillchar);
}

"""stringlib_center_impl: an odd margin puts the extra byte on the left
when the width is odd."""
def bl_center_impl(op: ptr[PyObject], width: i64, fillchar: u8) -> ptr[PyObject] {
    if bl_len(op) >= width {
        return bl_return_self(op);
    }
    marg = width - bl_len(op);
    left = marg // 2 + (marg & width & 1);
    return bl_pad(op, left, marg - left, fillchar);
}

"""stringlib_zfill_impl: pad with zeros on the left, moving a leading sign
to the front."""
def bl_zfill_impl(op: ptr[PyObject], width: i64) -> ptr[PyObject] {
    if bl_len(op) >= width {
        return bl_return_self(op);
    }
    fill = width - bl_len(op);
    s = bl_pad(op, fill, 0, CHAR_ZERO);
    if not s {
        return NULL;
    }
    p = bl_str(s);
    c = byte_at(p, fill);
    if c == CHAR_PLUS or c == CHAR_MINUS {
        # move sign to beginning of string
        set_byte(p, 0, c);
        set_byte(p, fill, CHAR_ZERO);
    }
    return s;
}

"""The width argument of ljust, rjust, center and zfill (a Py_ssize_t by
__index__), as (ok, width)."""
def width_arg(arg: ptr[PyObject]) -> tuple[bool, i64] {
    ival: i64 = -1;
    iobj = _PyNumber_Index(arg);
    if iobj {
        ival = PyLong_AsSsize_t(iobj);
        object_decref(iobj);
    }
    if ival == -1 and PyErr_Occurred() {
        return (False, ival);
    }
    return (True, ival);
}

"""The method name of a JUST_* parser."""
def just_name(which: i64) -> ptr[u8] {
    if which == JUST_LEFT {
        return ptr[u8]("ljust");
    }
    if which == JUST_RIGHT {
        return ptr[u8]("rjust");
    }
    return ptr[u8]("center");
}

"""_PyArg_CheckPositional(name, nargs, 1, 2) for a JUST_* parser."""
def just_check_positional(which: i64, nargs: i64) -> bool {
    if nargs >= 1 and nargs <= 2 {
        return True;
    }
    if which == JUST_LEFT {
        return _PyArg_CheckPositional("ljust", nargs, 1, 2) != i32(0);
    }
    if which == JUST_RIGHT {
        return _PyArg_CheckPositional("rjust", nargs, 1, 2) != i32(0);
    }
    return _PyArg_CheckPositional("center", nargs, 1, 2) != i32(0);
}

"""_PyArg_BadArgument for a fillchar that is not a byte string."""
def just_bad_fillchar(which: i64, arg: ptr[PyObject]) {
    if which == JUST_LEFT {
        _PyArg_BadArgument("ljust", "argument 2", "a byte string of length 1", arg);
    } elif which == JUST_RIGHT {
        _PyArg_BadArgument("rjust", "argument 2", "a byte string of length 1", arg);
    } else {
        _PyArg_BadArgument("center", "argument 2", "a byte string of length 1", arg);
    }
}

"""The fillchar argument (clinic's `char` converter): a bytes or bytearray
of length 1, as (ok, byte)."""
def fillchar_arg(which: i64, arg: ptr[PyObject]) -> tuple[bool, u8] {
    if type_has_feature(object_type(arg), Py_TPFLAGS_BYTES_SUBCLASS) {
        if object_size(arg) != 1 {
            PyErr_Format(
                PyExc_TypeError,
                "%s(): argument 2 must be a byte string of length 1, not a bytes object of length %zd",
                just_name(which),
                object_size(arg)
            );
            return (False, CHAR_SPACE);
        }
        return (True, byte_at(PyBytes_AsString(arg), 0));
    }
    if bytearray_check(arg) {
        if object_size(arg) != 1 {
            PyErr_Format(
                PyExc_TypeError,
                "%s(): argument 2 must be a byte string of length 1, not a bytearray object of length %zd",
                just_name(which),
                object_size(arg)
            );
            return (False, CHAR_SPACE);
        }
        return (True, byte_at(PyByteArray_AsString(arg), 0));
    }
    just_bad_fillchar(which, arg);
    return (False, CHAR_SPACE);
}

"""The clinic parser of ljust, rjust and center: (width, fillchar=b' ', /),
as (ok, width, fillchar)."""
def just_args(
    which: i64, args: ptr[ptr[PyObject]], nargs: i64
) -> tuple[bool, i64, u8] {
    if not just_check_positional(which, nargs) {
        return (False, 0, CHAR_SPACE);
    }
    (width_ok, width) = width_arg(args.view(1)[0]);
    if not width_ok {
        return (False, 0, CHAR_SPACE);
    }
    if nargs < 2 {
        return (True, width, CHAR_SPACE);
    }
    (fill_ok, fillchar) = fillchar_arg(which, (args + 1).view(1)[0]);
    if not fill_ok {
        return (False, 0, CHAR_SPACE);
    }
    return (True, width, fillchar);
}

"""stringlib_ljust (METH_FASTCALL)."""
def bl_ljust(op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64) -> ptr[PyObject] {
    (ok, width, fillchar) = just_args(JUST_LEFT, args, nargs);
    if not ok {
        return NULL;
    }
    return bl_ljust_impl(op, width, fillchar);
}

"""stringlib_rjust (METH_FASTCALL)."""
def bl_rjust(op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64) -> ptr[PyObject] {
    (ok, width, fillchar) = just_args(JUST_RIGHT, args, nargs);
    if not ok {
        return NULL;
    }
    return bl_rjust_impl(op, width, fillchar);
}

"""stringlib_center (METH_FASTCALL)."""
def bl_center(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    (ok, width, fillchar) = just_args(JUST_CENTER, args, nargs);
    if not ok {
        return NULL;
    }
    return bl_center_impl(op, width, fillchar);
}

"""stringlib_zfill (METH_O)."""
def bl_zfill(op: ptr[PyObject], arg: ptr[PyObject]) -> ptr[PyObject] {
    (ok, width) = width_arg(arg);
    if not ok {
        return NULL;
    }
    return bl_zfill_impl(op, width);
}

"""findchar: the offset of the first `c` in target[0:n], or -1 (C's
pointer, as an offset)."""
def findchar(target: ptr[u8], n: i64, c: u8) -> i64 {
    found = memchr(ptr(target), i32(c), u64(n));
    if found.is_null() {
        return -1;
    }
    return span(target, ptr[u8](found));
}

"""countchar: occurrences of `c` in target[0:target_len], stopping at
`maxcount`."""
def bl_countchar(target: ptr[u8], target_len: i64, c: u8, maxcount: i64) -> i64 {
    count: i64 = 0;
    start: i64 = 0;
    while True {
        offset = findchar(target + start, target_len - start, c);
        if offset < 0 {
            break;
        }
        count += 1;
        if count >= maxcount {
            break;
        }
        start = start + offset + 1;
    }
    return count;
}

def replace_overflow -> ptr[PyObject] {
    PyErr_SetString(PyExc_OverflowError, "replace bytes is too long");
    return NULL;
}

"""stringlib_replace_interleave: insert to_s before every byte and at the
end, at most `maxcount` times. len(self)>=1, from="", len(to)>=1,
maxcount>=1."""
def bl_replace_interleave(
    op: ptr[PyObject], to_s: ptr[u8], to_len: i64, maxcount: i64
) -> ptr[PyObject] {
    self_len = bl_len(op);
    # 1 at the end plus 1 after every character;
    # count = min(maxcount, self_len + 1)
    count = maxcount if maxcount <= self_len else self_len + 1;
    # Check for overflow: result_len = count * to_len + self_len
    if to_len > (PY_SSIZE_T_MAX - self_len) // count {
        return replace_overflow();
    }
    result_len = count * to_len + self_len;
    result = bl_new(bl_mutable(op), ptr[u8](), result_len);
    if not result {
        return NULL;
    }
    self_s = bl_str(op);
    result_s = bl_str(result);
    r: i64 = 0;
    i: i64 = 0;
    if to_len > 1 {
        # Lay the first one down (guaranteed this will occur)
        memcpy(ptr(result_s), ptr(to_s), u64(to_len));
        r += to_len;
        count -= 1;
        while i < count {
            set_byte(result_s, r, byte_at(self_s, i));
            r += 1;
            memcpy(ptr(result_s + r), ptr(to_s), u64(to_len));
            r += to_len;
            i += 1;
        }
    } else {
        set_byte(result_s, 0, byte_at(to_s, 0));
        r += to_len;
        count -= 1;
        while i < count {
            set_byte(result_s, r, byte_at(self_s, i));
            r += 1;
            set_byte(result_s, r, byte_at(to_s, 0));
            r += to_len;
            i += 1;
        }
    }
    # Copy the rest of the original string
    memcpy(ptr(result_s + r), ptr(self_s + i), u64(self_len - i));
    return result;
}

"""stringlib_replace_delete_single_character: len(self)>=1, len(from)==1,
to="", maxcount>=1."""
def bl_replace_delete_single_character(
    op: ptr[PyObject], from_c: u8, maxcount: i64
) -> ptr[PyObject] {
    self_len = bl_len(op);
    self_s = bl_str(op);
    count = bl_countchar(self_s, self_len, from_c, maxcount);
    if count == 0 {
        return bl_return_self(op);
    }
    # from_len == 1
    result_len = self_len - count;
    result = bl_new(bl_mutable(op), ptr[u8](), result_len);
    if not result {
        return NULL;
    }
    result_s = bl_str(result);
    r: i64 = 0;
    start: i64 = 0;
    while count > 0 {
        count -= 1;
        next = findchar(self_s + start, self_len - start, from_c);
        if next < 0 {
            break;
        }
        memcpy(ptr(result_s + r), ptr(self_s + start), u64(next));
        r += next;
        start = start + next + 1;
    }
    memcpy(ptr(result_s + r), ptr(self_s + start), u64(self_len - start));
    return result;
}

"""stringlib_replace_delete_substring: len(self)>=1, len(from)>=2, to="",
maxcount>=1."""
def bl_replace_delete_substring(
    op: ptr[PyObject], from_s: ptr[u8], from_len: i64, maxcount: i64
) -> ptr[PyObject] {
    self_len = bl_len(op);
    self_s = bl_str(op);
    count = bl_count(self_s, self_len, from_s, from_len, maxcount);
    if count == 0 {
        # no matches
        return bl_return_self(op);
    }
    result_len = self_len - (count * from_len);
    result = bl_new(bl_mutable(op), ptr[u8](), result_len);
    if not result {
        return NULL;
    }
    result_s = bl_str(result);
    r: i64 = 0;
    start: i64 = 0;
    while count > 0 {
        count -= 1;
        offset = bl_find(self_s + start, self_len - start, from_s, from_len, 0);
        if offset == -1 {
            break;
        }
        memcpy(ptr(result_s + r), ptr(self_s + start), u64(offset));
        r += offset;
        start = start + offset + from_len;
    }
    memcpy(ptr(result_s + r), ptr(self_s + start), u64(self_len - start));
    return result;
}

"""stringlib_replace_single_character_in_place: len(self)>=1,
len(from)==len(to)==1, maxcount>=1."""
def bl_replace_single_character_in_place(
    op: ptr[PyObject], from_c: u8, to_c: u8, maxcount: i64
) -> ptr[PyObject] {
    # The result string will be the same size
    self_s = bl_str(op);
    self_len = bl_len(op);
    next = findchar(self_s, self_len, from_c);
    if next < 0 {
        # No matches; return the original bytes
        return bl_return_self(op);
    }
    # Need to make a new bytes
    result = bl_new(bl_mutable(op), ptr[u8](), self_len);
    if not result {
        return NULL;
    }
    result_s = bl_str(result);
    memcpy(ptr(result_s), ptr(self_s), u64(self_len));
    # change everything in-place, starting with this one
    start = next;
    set_byte(result_s, start, to_c);
    start += 1;
    remaining = maxcount - 1;
    while remaining > 0 {
        next = findchar(result_s + start, self_len - start, from_c);
        if next < 0 {
            break;
        }
        set_byte(result_s, start + next, to_c);
        start = start + next + 1;
        remaining -= 1;
    }
    return result;
}

"""stringlib_replace_substring_in_place: len(self)>=1,
len(from)==len(to)>=2, maxcount>=1."""
def bl_replace_substring_in_place(
    op: ptr[PyObject],
    from_s: ptr[u8],
    from_len: i64,
    to_s: ptr[u8],
    to_len: i64,
    maxcount: i64
) -> ptr[PyObject] {
    # The result bytes will be the same size
    self_s = bl_str(op);
    self_len = bl_len(op);
    offset = bl_find(self_s, self_len, from_s, from_len, 0);
    if offset == -1 {
        # No matches; return the original bytes
        return bl_return_self(op);
    }
    # Need to make a new bytes
    result = bl_new(bl_mutable(op), ptr[u8](), self_len);
    if not result {
        return NULL;
    }
    result_s = bl_str(result);
    memcpy(ptr(result_s), ptr(self_s), u64(self_len));
    # change everything in-place, starting with this one
    start = offset;
    memcpy(ptr(result_s + start), ptr(to_s), u64(from_len));
    start += from_len;
    remaining = maxcount - 1;
    while remaining > 0 {
        offset = bl_find(result_s + start, self_len - start, from_s, from_len, 0);
        if offset == -1 {
            break;
        }
        memcpy(ptr(result_s + start + offset), ptr(to_s), u64(from_len));
        start += offset + from_len;
        remaining -= 1;
    }
    return result;
}

"""stringlib_replace_single_character: len(self)>=1, len(from)==1,
len(to)>=2, maxcount>=1."""
def bl_replace_single_character(
    op: ptr[PyObject], from_c: u8, to_s: ptr[u8], to_len: i64, maxcount: i64
) -> ptr[PyObject] {
    self_s = bl_str(op);
    self_len = bl_len(op);
    count = bl_countchar(self_s, self_len, from_c, maxcount);
    if count == 0 {
        # no matches, return unchanged
        return bl_return_self(op);
    }
    # use the difference between current and new, hence the "-1":
    # result_len = self_len + count * (to_len-1)
    if to_len - 1 > (PY_SSIZE_T_MAX - self_len) // count {
        return replace_overflow();
    }
    result_len = self_len + count * (to_len - 1);
    result = bl_new(bl_mutable(op), ptr[u8](), result_len);
    if not result {
        return NULL;
    }
    result_s = bl_str(result);
    r: i64 = 0;
    start: i64 = 0;
    while count > 0 {
        count -= 1;
        next = findchar(self_s + start, self_len - start, from_c);
        if next < 0 {
            break;
        }
        if next == 0 {
            # replace with the 'to'
            memcpy(ptr(result_s + r), ptr(to_s), u64(to_len));
            r += to_len;
            start += 1;
        } else {
            # copy the unchanged old then the 'to'
            memcpy(ptr(result_s + r), ptr(self_s + start), u64(next));
            r += next;
            memcpy(ptr(result_s + r), ptr(to_s), u64(to_len));
            r += to_len;
            start = start + next + 1;
        }
    }
    # Copy the remainder of the remaining bytes
    memcpy(ptr(result_s + r), ptr(self_s + start), u64(self_len - start));
    return result;
}

"""stringlib_replace_substring: len(self)>=1, len(from)>=2, len(to)>=2,
maxcount>=1."""
def bl_replace_substring(
    op: ptr[PyObject],
    from_s: ptr[u8],
    from_len: i64,
    to_s: ptr[u8],
    to_len: i64,
    maxcount: i64
) -> ptr[PyObject] {
    self_s = bl_str(op);
    self_len = bl_len(op);
    count = bl_count(self_s, self_len, from_s, from_len, maxcount);
    if count == 0 {
        # no matches, return unchanged
        return bl_return_self(op);
    }
    # Check for overflow: result_len = self_len + count * (to_len-from_len)
    if to_len - from_len > (PY_SSIZE_T_MAX - self_len) // count {
        return replace_overflow();
    }
    result_len = self_len + count * (to_len - from_len);
    result = bl_new(bl_mutable(op), ptr[u8](), result_len);
    if not result {
        return NULL;
    }
    result_s = bl_str(result);
    r: i64 = 0;
    start: i64 = 0;
    while count > 0 {
        count -= 1;
        offset = bl_find(self_s + start, self_len - start, from_s, from_len, 0);
        if offset == -1 {
            break;
        }
        if offset == 0 {
            # replace with the 'to'
            memcpy(ptr(result_s + r), ptr(to_s), u64(to_len));
            r += to_len;
            start += from_len;
        } else {
            # copy the unchanged old then the 'to'
            memcpy(ptr(result_s + r), ptr(self_s + start), u64(offset));
            r += offset;
            memcpy(ptr(result_s + r), ptr(to_s), u64(to_len));
            r += to_len;
            start = start + offset + from_len;
        }
    }
    # Copy the remainder of the remaining bytes
    memcpy(ptr(result_s + r), ptr(self_s + start), u64(self_len - start));
    return result;
}

"""stringlib_replace: `op` with up to `maxcount` (all when negative)
occurrences of from_s[0:from_len] replaced by to_s[0:to_len]."""
def bl_replace(
    op: ptr[PyObject],
    from_s: ptr[u8],
    from_len: i64,
    to_s: ptr[u8],
    to_len: i64,
    maxcount_in: i64
) -> ptr[PyObject] {
    if bl_len(op) < from_len {
        # nothing to do; return the original bytes
        return bl_return_self(op);
    }
    maxcount = maxcount_in;
    if maxcount < 0 {
        maxcount = PY_SSIZE_T_MAX;
    } elif maxcount == 0 {
        # nothing to do; return the original bytes
        return bl_return_self(op);
    }
    # Handle zero-length special cases
    if from_len == 0 {
        if to_len == 0 {
            # nothing to do; return the original bytes
            return bl_return_self(op);
        }
        # insert the 'to' bytes everywhere:
        # b"Python".replace(b"", b".") == b'.P.y.t.h.o.n.'
        return bl_replace_interleave(op, to_s, to_len, maxcount);
    }
    if to_len == 0 {
        # delete all occurrences of 'from' bytes
        if from_len == 1 {
            return bl_replace_delete_single_character(op, byte_at(from_s, 0), maxcount);
        }
        return bl_replace_delete_substring(op, from_s, from_len, maxcount);
    }
    # Handle special case where both bytes have the same length
    if from_len == to_len {
        if from_len == 1 {
            return bl_replace_single_character_in_place(
                op, byte_at(from_s, 0), byte_at(to_s, 0), maxcount
            );
        }
        return bl_replace_substring_in_place(
            op, from_s, from_len, to_s, to_len, maxcount
        );
    }
    # Otherwise use the more generic algorithms
    if from_len == 1 {
        return bl_replace_single_character(
            op, byte_at(from_s, 0), to_s, to_len, maxcount
        );
    }
    # len('from')>=2, len('to')>=1
    return bl_replace_substring(op, from_s, from_len, to_s, to_len, maxcount);
}
