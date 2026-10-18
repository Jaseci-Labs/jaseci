"""json.dumps walks multibyte text once and escapes it the way CPython does."""
import json;

def run -> int {
    big = "日本" * 40000 + "é \"q\"";
    print(len(json.dumps(big)), len(json.dumps(big, ensure_ascii=False)));
    for w in ["héllo", "日本語", "🙂x🙂", "abc", "", "è\n"] {
        print(json.dumps(w), json.dumps(w, ensure_ascii=False));
    }
    print(json.dumps("tab\t \"q\" \\ é 🙂 \x7f end"));
    print(json.dumps("tab\t é 🙂 \x7f end", ensure_ascii=False));
    return len(big);
}

with entry {
    print(run());
}
