const { Prism } = require("prism-react-renderer")

Prism.languages.jac = {
    'comment': {
        pattern: /(^|[^\\])\/\/.*/,
        lookbehind: true,
        greedy: true
    },
    'keyword': /\b(?:(^\\s|:?\\s|)(\\w+|\\w+(?:\\.\\w+)+)\\s*(=|\\+=|-=|\\+\\+|--)\\s*|\s*\\b(?<!\\.)(node|walker)\\b(?=.*[:\\\\])|\s*\\b(?<!\\.)()\\b(?=.*[-\\\\])|node|walker|report|destroy|here|take|in|has|can|anchor|private|not|and|or|import|ignore|with|strict|context|details|info|activity|length|keys|str|int|float|list|dict|bool|edge|digraph|subgraph|test|type|if|elif|else|while|for|while|in|by|to|report|take|ignore|skip|disengage|break|continue|destroy|spawn|entry|exit|assert)\b/,
    'boolean': /\b(?:false|null|true)\b/,
    'number': /\b0(?:b(?:_?[01])+|o(?:_?[0-7])+|x(?:_?[a-f0-9])+)\b|(?:\b\d+(?:_\d+)*(?:\.(?:\d+(?:_\d+)*)?)?|\B\.\d+(?:_\d+)*)(?:e[+-]?\d+(?:_\d+)*)?j?(?!\w)/i,
    'operator': /[*\/%^!=]=?|\+[=+]?|-[=-]?|\|[=|]?|&(?:=|&|\^=?)?|>(?:>=?|=)?|<(?:<=?|=|-)?|:=|\.\.\./,
    'punctuation': /[{}[\];(),.:]/
}

Prism.languages.jac = Prism.languages.jac;
