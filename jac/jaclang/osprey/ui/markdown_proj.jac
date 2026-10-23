"""Markdown as transcript projection — domain text → styled spans/lines.

Not a component tree and not markup authoring. Lexer is intentionally small:
headings, fences, lists, hr, and inline bold/italic/code/strike. Output feeds
cell blit / transcript spans (OSPUI §16).
"""

import re;

import from .cells {
    StyleAttrs,
}

import from .width {
    wrap_text,
    display_width,
}


obj ProjSpan {
    has text: str = "",
        style_id: str = "default",
        attrs: StyleAttrs = StyleAttrs();
}


obj ProjLine {
    has spans: list[ProjSpan] = [];
}


glob _HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$");
glob _FENCE_RE = re.compile(r"^(`{3,}|~{3,})(.*)$");
glob _HR_RE = re.compile(r"^(\s*([-*_]\s*){3,})$");
glob _UL_RE = re.compile(r"^(\s*)([-*+])\s+(.*)$");
glob _OL_RE = re.compile(r"^(\s*)(\d{1,9})[.)]\s+(.*)$");
glob _INLINE_RE = re.compile(
    r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|~~[^~]+~~)"
);


def style_attrs_for(style_id: str) -> StyleAttrs {
    if style_id == "heading" {
        return StyleAttrs(bold=True, fg=6);
    }
    if style_id == "strong" {
        return StyleAttrs(bold=True);
    }
    if style_id == "em" {
        return StyleAttrs(italic=True);
    }
    if style_id == "code" or style_id == "codespan" {
        return StyleAttrs(fg=3);
    }
    if style_id == "strike" {
        return StyleAttrs(dim=True);
    }
    if style_id == "list_marker" {
        return StyleAttrs(fg=4);
    }
    if style_id == "hr" {
        return StyleAttrs(dim=True);
    }
    if style_id == "blockquote" {
        return StyleAttrs(dim=True, italic=True);
    }
    return StyleAttrs();
}


def _span(text: str, style_id: str = "default") -> ProjSpan {
    return ProjSpan(
        text=text,
        style_id=style_id,
        attrs=style_attrs_for(style_id),
    );
}


"""Split one plain line into inline styled spans."""
def project_inline_spans(text: str) -> list[ProjSpan] {
    if not text {
        return [_span("")];
    }
    out: list[ProjSpan] = [];
    i = 0;
    for m in _INLINE_RE.finditer(text) {
        start = m.start();
        end = m.end();
        if start > i {
            out.append(_span(text[i:start], "default"));
        }
        raw = m.group(0);
        if raw.startswith("**") and raw.endswith("**") and len(raw) >= 4 {
            out.append(_span(raw[2:-2], "strong"));
        } elif raw.startswith("~~") and raw.endswith("~~") and len(raw) >= 4 {
            out.append(_span(raw[2:-2], "strike"));
        } elif raw.startswith("`") and raw.endswith("`") and len(raw) >= 2 {
            out.append(_span(raw[1:-1], "codespan"));
        } elif raw.startswith("*") and raw.endswith("*") and len(raw) >= 2 {
            out.append(_span(raw[1:-1], "em"));
        } else {
            out.append(_span(raw, "default"));
        }
        i = end;
    }
    if i < len(text) {
        out.append(_span(text[i:], "default"));
    }
    if not out {
        out.append(_span(text, "default"));
    }
    return out;
}


def _line_plain(text: str, style_id: str = "default") -> ProjLine {
    return ProjLine(spans=[_span(text, style_id)]);
}


def _line_inline(text: str) -> ProjLine {
    return ProjLine(spans=project_inline_spans(text));
}


"""Project markdown source into display lines of styled spans (no OSP nodes)."""
def project_markdown(source: str, width: int = 80) -> list[ProjLine] {
    lines_out: list[ProjLine] = [];
    if not source {
        return [_line_plain("")];
    }
    raw_lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n");
    i = 0;
    n = len(raw_lines);
    in_fence = False;
    fence_marker = "";
    while i < n {
        line = raw_lines[i];
        if in_fence {
            if line.startswith(fence_marker) {
                in_fence = False;
                fence_marker = "";
            } else {
                for wrapped in wrap_text(line if line else " ", max(1, width)) {
                    lines_out.append(_line_plain(wrapped, "code"));
                }
            }
            i += 1;
            continue;
        }
        fence = _FENCE_RE.match(line);
        if fence {
            in_fence = True;
            fence_marker = fence.group(1)[0] * len(fence.group(1));
            i += 1;
            continue;
        }
        if _HR_RE.match(line.strip()) and len(line.strip()) >= 3 {
            rule = "─" * max(1, min(width, 40));
            lines_out.append(_line_plain(rule, "hr"));
            i += 1;
            continue;
        }
        heading = _HEADING_RE.match(line);
        if heading {
            body = heading.group(2);
            for wrapped in wrap_text(body, max(1, width)) {
                lines_out.append(_line_plain(wrapped, "heading"));
            }
            i += 1;
            continue;
        }
        if line.startswith(">") {
            body = line[1:];
            if body.startswith(" ") {
                body = body[1:];
            }
            prefix = "│ ";
            room = max(1, width - display_width(prefix));
            for wrapped in wrap_text(body if body else " ", room) {
                spans = [_span(prefix, "blockquote")] + project_inline_spans(
                    wrapped
                );
                # Dim the body too.
                for s in spans[1:] {
                    if s.style_id == "default" {
                        s.style_id = "blockquote";
                        s.attrs = style_attrs_for("blockquote");
                    }
                }
                lines_out.append(ProjLine(spans=spans));
            }
            i += 1;
            continue;
        }
        ul = _UL_RE.match(line);
        if ul {
            body = ul.group(3);
            marker = "• ";
            room = max(1, width - display_width(marker));
            first = True;
            for wrapped in wrap_text(body if body else " ", room) {
                if first {
                    spans = [_span(marker, "list_marker")] + project_inline_spans(
                        wrapped
                    );
                    first = False;
                } else {
                    spans = [_span("  ", "default")] + project_inline_spans(
                        wrapped
                    );
                }
                lines_out.append(ProjLine(spans=spans));
            }
            i += 1;
            continue;
        }
        ol = _OL_RE.match(line);
        if ol {
            body = ol.group(3);
            marker = ol.group(2) + ". ";
            room = max(1, width - display_width(marker));
            first = True;
            for wrapped in wrap_text(body if body else " ", room) {
                if first {
                    spans = [_span(marker, "list_marker")] + project_inline_spans(
                        wrapped
                    );
                    first = False;
                } else {
                    pad = " " * display_width(marker);
                    spans = [_span(pad, "default")] + project_inline_spans(
                        wrapped
                    );
                }
                lines_out.append(ProjLine(spans=spans));
            }
            i += 1;
            continue;
        }
        if not line.strip() {
            lines_out.append(_line_plain(""));
            i += 1;
            continue;
        }
        for wrapped in wrap_text(line, max(1, width)) {
            lines_out.append(_line_inline(wrapped));
        }
        i += 1;
    }
    if not lines_out {
        lines_out.append(_line_plain(""));
    }
    return lines_out;
}


"""Flatten projected lines to the span dicts used by transcript / blit."""
def proj_lines_to_span_dicts(lines: list[ProjLine]) -> list[dict[str, any]] {
    out: list[dict[str, any]] = [];
    for line in lines {
        texts: list[str] = [];
        style = "default";
        if line.spans {
            style = line.spans[0].style_id;
            for s in line.spans {
                texts.append(s.text);
            }
        }
        out.append({"text": "".join(texts), "style_id": style, "spans": line.spans});
    }
    return out;
}


"""True when content likely benefits from markdown projection."""
def looks_like_markdown(text: str) -> bool {
    if not text {
        return False;
    }
    if text.startswith("#") {
        return True;
    }
    if "```" in text or "~~" in text {
        return True;
    }
    if "**" in text or "`" in text {
        return True;
    }
    for line in text.split("\n") {
        s = line.strip();
        if s.startswith("- ") or s.startswith("* ") or s.startswith("> ") {
            return True;
        }
        if _OL_RE.match(line) {
            return True;
        }
    }
    return False;
}
