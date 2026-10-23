"""Pure string edit engine - no I/O.

Anchor-free module: the placement solver should decide it native. This is the
N1 dogfooding module; tools.jac calls it across the server/native bridge.

Error convention (shared by every function): failures return "ERROR: ..."
strings instead of raising, so callers can surface them to the model without
exceptions. Functions never mutate their inputs.
"""

"""Replace old_text with new_text in source. old_text must appear exactly once.

Returns the new source on success, or an "ERROR: ..." string describing the
failure so callers can surface it to the model without exceptions.
"""
def apply_edit(source: str, old_text: str, new_text: str) -> str {
    if len(old_text) == 0 {
        return "ERROR: old_text is empty";
    }
    first = source.find(old_text);
    if first == -1 {
        return "ERROR: old_text not found in file";
    }
    second = source.find(old_text, first + len(old_text));
    if second != -1 {
        return "ERROR: old_text matches more than once; add surrounding context to make it unique";
    }
    return source[:first] + new_text + source[first + len(old_text):];
}

"""Apply a sequential list of [old_text, new_text] edit pairs to source.

Pairs are applied in order, each against the result of the previous one.
Atomic: if ANY pair fails, an "ERROR: ..." string identifying the failing
pair index (1-based) is returned and the caller receives no partial result;
since this module is pure, the original "source" is never mutated.
An empty edits list returns source unchanged.
"""
def apply_multi_edit(source: str, edits: list[list[str]]) -> str {
    work = source;
    for i in range(len(edits)) {
        pair = edits[i];
        old_text: str = pair[0];
        new_text: str = pair[1];
        result = apply_edit(work, old_text, new_text);
        if result.startswith("ERROR:") {
            return "ERROR: multi-edit pair "
                + str(i + 1) + " of " + str(len(edits)) + " failed: " + result;
        }
        work = result;
    }
    return work;
}

"""Replace the 1-based inclusive line range [start_line, end_line] with
replacement text.

Newline handling: the file is split into newline-free lines; a trailing
newline in the source is preserved on the result (dropped only when the
edit empties the whole file). Bounds violations (start < 1, start > line
count, end < start, end > line count) return "ERROR: ..." strings.
An empty replacement deletes the range. An empty source has no lines, so any
range is out of bounds.
"""
def replace_lines(source: str, start_line: int, end_line: int, replacement: str) -> str {
    # splitlines() is unreliable in this runtime; split on newlines directly
    # and drop the empty piece a trailing newline produces.
    lines = source.split("\n");
    trailing_nl = False;
    if len(lines) > 0 and lines[-1] == "" {
        trailing_nl = True;
        lines = lines[:-1];
    }
    n = len(lines);
    if start_line < 1 or start_line > n {
        return "ERROR: start_line " + str(start_line)
            + " out of range (file has " + str(n) + " lines)";
    }
    if end_line < start_line {
        return "ERROR: end_line " + str(end_line)
            + " is before start_line " + str(start_line);
    }
    if end_line > n {
        return "ERROR: end_line " + str(end_line)
            + " out of range (file has " + str(n) + " lines)";
    }
    repl_lines = replacement.split("\n");
    if replacement == "" {
        repl_lines = [];
    }
    out_lines = lines[:start_line - 1] + repl_lines + lines[end_line:];
    text = "\n".join(out_lines);
    if len(out_lines) > 0 and trailing_nl {
        text += "\n";
    }
    return text;
}

"""Count non-overlapping occurrences of needle in source, using str.count
semantics: after a match, scanning resumes past its end. An empty needle
counts as 0 matches.
"""
def count_matches(source: str, needle: str) -> int {
    if len(needle) == 0 {
        return 0;
    }
    count = 0;
    pos = source.find(needle);
    while pos != -1 {
        count += 1;
        pos = source.find(needle, pos + len(needle));
    }
    return count;
}

"""Minimal unified diff between old_text and new_text.

Hand-rolled LCS hunks (difflib.unified_diff cannot lower in the native
codespace, and this module is pinned native). Output follows Python-difflib
conventions: at-sign hunk headers with ranges, single-line ranges omit the
length suffix, and 0-length old ranges report the preceding line number.
Space, minus and plus line prefixes; context unchanged lines around each
hunk. Identical inputs produce the empty string. Negative context is
rejected with an ERROR string.
"""
def compute_unified_diff(old_text: str, new_text: str, context: int = 3) -> str {
    if context < 0 {
        return "ERROR: context must be >= 0";
    }
    old_lines = old_text.split("\n");
    if len(old_lines) > 0 and old_lines[-1] == "" {
        old_lines = old_lines[:-1];
    }
    new_lines = new_text.split("\n");
    if len(new_lines) > 0 and new_lines[-1] == "" {
        new_lines = new_lines[:-1];
    }
    n = len(old_lines);
    m = len(new_lines);

    # LCS table: lcs[i][j] = LCS length of old_lines[i:] vs new_lines[j:].
    lcs: list[list[int]] = [];
    for i in range(n + 1) {
        row: list[int] = [];
        for j in range(m + 1) {
            row.append(0);
        }
        lcs.append(row);
    }
    for i in range(n - 1, -1, -1) {
        for j in range(m - 1, -1, -1) {
            if old_lines[i] == new_lines[j] {
                lcs[i][j] = lcs[i + 1][j + 1] + 1;
            } elif lcs[i + 1][j] >= lcs[i][j + 1] {
                lcs[i][j] = lcs[i + 1][j];
            } else {
                lcs[i][j] = lcs[i][j + 1];
            }
        }
    }

    # Flatten into per-line ops: e equal, d delete-from-old, a add-from-new.
    tags: list[str] = [];
    old_idx: list[int] = [];
    new_idx: list[int] = [];
    oi = 0;
    oj = 0;
    while oi < n and oj < m {
        if old_lines[oi] == new_lines[oj] {
            tags.append("e");
            old_idx.append(oi);
            new_idx.append(oj);
            oi += 1;
            oj += 1;
        } elif lcs[oi + 1][oj] >= lcs[oi][oj + 1] {
            tags.append("d");
            old_idx.append(oi);
            new_idx.append(oj);
            oi += 1;
        } else {
            tags.append("a");
            old_idx.append(oi);
            new_idx.append(oj);
            oj += 1;
        }
    }
    while oi < n {
        tags.append("d");
        old_idx.append(oi);
        new_idx.append(oj);
        oi += 1;
    }
    while oj < m {
        tags.append("a");
        old_idx.append(oi);
        new_idx.append(oj);
        oj += 1;
    }

    K = len(tags);
    out: list[str] = [];
    k = 0;
    while k < K and tags[k] == "e" {
        k += 1;
    }
    while k < K {
        ws = k - context;
        if ws < 0 {
            ws = 0;
        }
        le = k;
        j = k;
        while j < K {
            if tags[j] != "e" {
                le = j;
                j += 1;
                continue;
            }
            r = j;
            while r < K and tags[r] == "e" {
                r += 1;
            }
            if r < K and (r - j) <= 2 * context {
                j = r;
                continue;
            }
            break;
        }
        we = le + 1 + context;
        if we > K {
            we = K;
        }

        # Header ranges over the window.
        first_old = -1;
        last_old = -1;
        first_new = -1;
        last_new = -1;
        old_len = 0;
        new_len = 0;
        for t in range(ws, we) {
            if tags[t] != "a" {
                old_len += 1;
                if first_old == -1 {
                    first_old = old_idx[t];
                }
                last_old = old_idx[t];
            }
            if tags[t] != "d" {
                new_len += 1;
                if first_new == -1 {
                    first_new = new_idx[t];
                }
                last_new = new_idx[t];
            }
        }
        old_start = first_old + 1;
        if old_len == 0 {
            old_start -= 1;
        }
        new_start = first_new + 1;
        if new_len == 0 {
            new_start -= 1;
        }
        out.append(
            "@@ -" + _fmt_range(old_start, old_len)
            + " +" + _fmt_range(new_start, new_len) + " @@"
        );
        for t in range(ws, we) {
            if tags[t] == "e" {
                out.append(" " + old_lines[old_idx[t]]);
            } elif tags[t] == "d" {
                out.append("-" + old_lines[old_idx[t]]);
            } else {
                out.append("+" + new_lines[new_idx[t]]);
            }
        }

        k = we;
        while k < K and tags[k] == "e" {
            k += 1;
        }
    }
    return "\n".join(out);
}

"""Format one side of an @@ header following Python-difflib conventions.
"""
def _fmt_range(start: int, length: int) -> str {
    if length == 1 {
        return str(start);
    }
    if length == 0 {
        return str(start - 1) + ",0";
    }
    return str(start) + "," + str(length);
}

"""Detect the dominant indentation unit of source for smart insertions.

Counts indented lines whose leading whitespace starts with a tab vs spaces.
Tabs win only when strictly more numerous than space-indented lines; ties and
space majorities prefer a space unit sized by the GCD of observed indent
widths (typically 4 spaces). No indented lines yields the empty string
(unknown; callers should fall back to their default).
"""
def guess_indentation(source: str) -> str {
    tab_lines = 0;
    widths = [];
    for line in source.splitlines() {
        stripped = line.lstrip(" \t");
        lead = line[:len(line) - len(stripped)];
        if len(stripped) == 0 or len(lead) == 0 {
            continue;
        }
        if lead[0] == "\t" {
            tab_lines += 1;
        } else {
            widths.append(len(lead));
        }
    }
    if len(widths) == 0 {
        if tab_lines > 0 {
            return "\t";
        }
        return "";
    }
    if tab_lines > len(widths) {
        return "\t";
    }
    unit = widths[0];
    for w in widths[1:] {
        a = unit;
        b = w;
        while b != 0 {
            tmp = a % b;
            a = b;
            b = tmp;
        }
        unit = a;
    }
    if unit == 0 {
        unit = 4;
    }
    return " " * unit;
}
