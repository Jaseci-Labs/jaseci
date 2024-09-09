import abc
import logging
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from collections.abc import Generator
from types import ModuleType
from typing import (
    Any,
    Callable,
    ClassVar,
    Collection,
    Generic,
    IO,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
    TypeVar,
    overload,
)

__version__: str

class LarkError(Exception): ...
class ConfigurationError(LarkError, ValueError): ...

def assert_config(
    value, options: Collection, msg: str = "Got %r, expected one of %s"
): ...

class GrammarError(LarkError): ...
class ParseError(LarkError): ...
class LexError(LarkError): ...

T = TypeVar("T")

class UnexpectedInput(LarkError):
    line: int
    column: int
    pos_in_stream: Incomplete
    state: Any
    interactive_parser: InteractiveParser
    def get_context(self, text: str, span: int = 40) -> str: ...
    def match_examples(
        self,
        parse_fn: Callable[[str], Tree],
        examples: Mapping[T, Iterable[str]] | Iterable[tuple[T, Iterable[str]]],
        token_type_match_fallback: bool = False,
        use_accepts: bool = True,
    ) -> T | None: ...

class UnexpectedEOF(ParseError, UnexpectedInput):
    expected: list[Token]
    state: Incomplete
    token: Incomplete
    pos_in_stream: int
    line: int
    column: int
    def __init__(
        self,
        expected,
        state: Incomplete | None = None,
        terminals_by_name: Incomplete | None = None,
    ) -> None: ...

class UnexpectedCharacters(LexError, UnexpectedInput):
    allowed: set[str]
    considered_tokens: set[Any]
    line: Incomplete
    column: Incomplete
    pos_in_stream: Incomplete
    state: Incomplete
    considered_rules: Incomplete
    token_history: Incomplete
    char: Incomplete
    def __init__(
        self,
        seq,
        lex_pos,
        line,
        column,
        allowed: Incomplete | None = None,
        considered_tokens: Incomplete | None = None,
        state: Incomplete | None = None,
        token_history: Incomplete | None = None,
        terminals_by_name: Incomplete | None = None,
        considered_rules: Incomplete | None = None,
    ) -> None: ...

class UnexpectedToken(ParseError, UnexpectedInput):
    expected: set[str]
    considered_rules: set[str]
    line: Incomplete
    column: Incomplete
    pos_in_stream: Incomplete
    state: Incomplete
    token: Incomplete
    interactive_parser: Incomplete
    token_history: Incomplete
    def __init__(
        self,
        token,
        expected,
        considered_rules: Incomplete | None = None,
        state: Incomplete | None = None,
        interactive_parser: Incomplete | None = None,
        terminals_by_name: Incomplete | None = None,
        token_history: Incomplete | None = None,
    ) -> None: ...
    @property
    def accepts(self) -> set[str]: ...

class VisitError(LarkError):
    obj: Tree | Token
    orig_exc: Exception
    rule: Incomplete
    def __init__(self, rule, obj, orig_exc) -> None: ...

class MissingVariableError(LarkError): ...

logger: logging.Logger
NO_VALUE: Incomplete
T = TypeVar("T")

def classify(
    seq: Iterable, key: Callable | None = None, value: Callable | None = None
) -> dict: ...

class Serialize:
    def memo_serialize(self, types_to_memoize: list) -> Any: ...
    def serialize(self, memo: Incomplete | None = None) -> dict[str, Any]: ...
    @classmethod
    def deserialize(cls, data: dict[str, Any], memo: dict[int, Any]) -> _T: ...

class SerializeMemoizer(Serialize):
    __serialize_fields__: Incomplete
    types_to_memoize: Incomplete
    memoized: Incomplete
    def __init__(self, types_to_memoize: list) -> None: ...
    def in_types(self, value: Serialize) -> bool: ...
    def serialize(self) -> dict[int, Any]: ...
    @classmethod
    def deserialize(
        cls, data: dict[int, Any], namespace: dict[str, Any], memo: dict[Any, Any]
    ) -> dict[int, Any]: ...

categ_pattern: Incomplete

def get_regexp_width(expr: str) -> tuple[int, int] | list[int]: ...

class Meta:
    empty: bool
    line: int
    column: int
    start_pos: int
    end_line: int
    end_column: int
    end_pos: int
    orig_expansion: list[TerminalDef]
    match_tree: bool
    def __init__(self) -> None: ...

Branch: Incomplete

class Tree(Generic[_Leaf_T]):
    data: str
    children: list[Branch[_Leaf_T]]
    def __init__(
        self, data: str, children: list[Branch[_Leaf_T]], meta: Meta | None = None
    ) -> None: ...
    @property
    def meta(self) -> Meta: ...
    def pretty(self, indent_str: str = "  ") -> str: ...
    def __rich__(self, parent: rich.tree.Tree | None = None) -> rich.tree.Tree: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self) -> int: ...
    def iter_subtrees(self) -> Iterator[Tree[_Leaf_T]]: ...
    def iter_subtrees_topdown(self) -> Generator[Incomplete, None, None]: ...
    def find_pred(
        self, pred: Callable[[Tree[_Leaf_T]], bool]
    ) -> Iterator[Tree[_Leaf_T]]: ...
    def find_data(self, data: str) -> Iterator[Tree[_Leaf_T]]: ...

class _DiscardType: ...

Discard: Incomplete

class _Decoratable:
    def __class_getitem__(cls, _): ...

class Transformer(_Decoratable, ABC, Generic[_Leaf_T, _Return_T]):
    __visit_tokens__: bool
    def __init__(self, visit_tokens: bool = True) -> None: ...
    def transform(self, tree: Tree[_Leaf_T]) -> _Return_T: ...
    def __mul__(
        self,
        other: Transformer[_Leaf_U, _Return_V] | TransformerChain[_Leaf_U, _Return_V],
    ) -> TransformerChain[_Leaf_T, _Return_V]: ...
    def __default__(self, data, children, meta): ...
    def __default_token__(self, token): ...

def merge_transformers(
    base_transformer: Incomplete | None = None, **transformers_to_merge
): ...

class InlineTransformer(Transformer): ...

class TransformerChain(Generic[_Leaf_T, _Return_T]):
    transformers: tuple[Transformer | TransformerChain, ...]
    def __init__(self, *transformers: Transformer | TransformerChain) -> None: ...
    def transform(self, tree: Tree[_Leaf_T]) -> _Return_T: ...
    def __mul__(
        self,
        other: Transformer[_Leaf_U, _Return_V] | TransformerChain[_Leaf_U, _Return_V],
    ) -> TransformerChain[_Leaf_T, _Return_V]: ...

class Transformer_InPlace(Transformer[_Leaf_T, _Return_T]):
    def transform(self, tree: Tree[_Leaf_T]) -> _Return_T: ...

class Transformer_NonRecursive(Transformer[_Leaf_T, _Return_T]):
    def transform(self, tree: Tree[_Leaf_T]) -> _Return_T: ...

class Transformer_InPlaceRecursive(Transformer): ...

class VisitorBase:
    def __default__(self, tree): ...
    def __class_getitem__(cls, _): ...

class Visitor(VisitorBase, ABC, Generic[_Leaf_T]):
    def visit(self, tree: Tree[_Leaf_T]) -> Tree[_Leaf_T]: ...
    def visit_topdown(self, tree: Tree[_Leaf_T]) -> Tree[_Leaf_T]: ...

class Visitor_Recursive(VisitorBase, Generic[_Leaf_T]):
    def visit(self, tree: Tree[_Leaf_T]) -> Tree[_Leaf_T]: ...
    def visit_topdown(self, tree: Tree[_Leaf_T]) -> Tree[_Leaf_T]: ...

class Interpreter(_Decoratable, ABC, Generic[_Leaf_T, _Return_T]):
    def visit(self, tree: Tree[_Leaf_T]) -> _Return_T: ...
    def visit_children(self, tree: Tree[_Leaf_T]) -> list: ...
    def __getattr__(self, name): ...
    def __default__(self, tree): ...

def visit_children_decor(func: _InterMethod) -> _InterMethod: ...

class _VArgsWrapper:
    base_func: Callable
    visit_wrapper: Incomplete
    def __init__(
        self, func: Callable, visit_wrapper: Callable[[Callable, str, list, Any], Any]
    ) -> None: ...
    def __call__(self, *args, **kwargs): ...
    def __get__(self, instance, owner: Incomplete | None = None): ...
    def __set_name__(self, owner, name) -> None: ...

def v_args(
    inline: bool = False,
    meta: bool = False,
    tree: bool = False,
    wrapper: Callable | None = None,
) -> Callable[[_DECORATED], _DECORATED]: ...

TOKEN_DEFAULT_PRIORITY: int

class Symbol(Serialize):
    name: str
    is_term: ClassVar[bool]
    def __init__(self, name: str) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self): ...
    fullrepr: Incomplete
    def renamed(self, f): ...

class Terminal(Symbol):
    __serialize_fields__: Incomplete
    is_term: ClassVar[bool]
    name: Incomplete
    filter_out: Incomplete
    def __init__(self, name, filter_out: bool = False) -> None: ...
    @property
    def fullrepr(self): ...
    def renamed(self, f): ...

class NonTerminal(Symbol):
    __serialize_fields__: Incomplete
    is_term: ClassVar[bool]

class RuleOptions(Serialize):
    __serialize_fields__: Incomplete
    keep_all_tokens: bool
    expand1: bool
    priority: int | None
    template_source: str | None
    empty_indices: tuple[bool, ...]
    def __init__(
        self,
        keep_all_tokens: bool = False,
        expand1: bool = False,
        priority: int | None = None,
        template_source: str | None = None,
        empty_indices: tuple[bool, ...] = (),
    ) -> None: ...

class Rule(Serialize):
    __serialize_fields__: Incomplete
    __serialize_namespace__: Incomplete
    origin: NonTerminal
    expansion: Sequence[Symbol]
    order: int
    alias: str | None
    options: RuleOptions
    def __init__(
        self,
        origin: NonTerminal,
        expansion: Sequence[Symbol],
        order: int = 0,
        alias: str | None = None,
        options: RuleOptions | None = None,
    ) -> None: ...
    def __hash__(self): ...
    def __eq__(self, other): ...

has_interegular: Incomplete

class Pattern(Serialize, ABC, metaclass=abc.ABCMeta):
    value: str
    flags: Collection[str]
    raw: str | None
    type: ClassVar[str]
    def __init__(
        self, value: str, flags: Collection[str] = (), raw: str | None = None
    ) -> None: ...
    def __hash__(self): ...
    def __eq__(self, other): ...
    @abstractmethod
    def to_regexp(self) -> str: ...
    @property
    @abstractmethod
    def min_width(self) -> int: ...
    @property
    @abstractmethod
    def max_width(self) -> int: ...

class PatternStr(Pattern):
    __serialize_fields__: Incomplete
    type: ClassVar[str]
    def to_regexp(self) -> str: ...
    @property
    def min_width(self) -> int: ...
    @property
    def max_width(self) -> int: ...

class PatternRE(Pattern):
    __serialize_fields__: Incomplete
    type: ClassVar[str]
    def to_regexp(self) -> str: ...
    @property
    def min_width(self) -> int: ...
    @property
    def max_width(self) -> int: ...

class TerminalDef(Serialize):
    __serialize_fields__: Incomplete
    __serialize_namespace__: Incomplete
    name: str
    pattern: Pattern
    priority: int
    def __init__(self, name: str, pattern: Pattern, priority: int = ...) -> None: ...
    def user_repr(self) -> str: ...

class Token(str):
    __match_args__: Incomplete
    type: str
    start_pos: int | None
    value: Any
    line: int | None
    column: int | None
    end_line: int | None
    end_column: int | None
    end_pos: int | None
    @overload
    def __new__(
        cls,
        type: str,
        value: Any,
        start_pos: int | None = None,
        line: int | None = None,
        column: int | None = None,
        end_line: int | None = None,
        end_column: int | None = None,
        end_pos: int | None = None,
    ) -> Token: ...
    @overload
    def __new__(
        cls,
        type_: str,
        value: Any,
        start_pos: int | None = None,
        line: int | None = None,
        column: int | None = None,
        end_line: int | None = None,
        end_column: int | None = None,
        end_pos: int | None = None,
    ) -> Token: ...
    @overload
    def update(self, type: str | None = None, value: Any | None = None) -> Token: ...
    @overload
    def update(self, type_: str | None = None, value: Any | None = None) -> Token: ...
    @classmethod
    def new_borrow_pos(cls, type_: str, value: Any, borrow_t: Token) -> _T: ...
    def __reduce__(self): ...
    def __deepcopy__(self, memo): ...
    def __eq__(self, other): ...
    __hash__: Incomplete

class LineCounter:
    newline_char: Incomplete
    char_pos: int
    line: int
    column: int
    line_start_pos: int
    def __init__(self, newline_char) -> None: ...
    def __eq__(self, other): ...
    def feed(self, token: Token, test_newline: bool = True): ...

class UnlessCallback:
    scanner: Incomplete
    def __init__(self, scanner) -> None: ...
    def __call__(self, t): ...

class CallChain:
    callback1: Incomplete
    callback2: Incomplete
    cond: Incomplete
    def __init__(self, callback1, callback2, cond) -> None: ...
    def __call__(self, t): ...

class Scanner:
    terminals: Incomplete
    g_regex_flags: Incomplete
    re_: Incomplete
    use_bytes: Incomplete
    match_whole: Incomplete
    allowed_types: Incomplete
    def __init__(
        self, terminals, g_regex_flags, re_, use_bytes, match_whole: bool = False
    ) -> None: ...
    def match(self, text, pos): ...

class LexerState:
    text: str
    line_ctr: LineCounter
    last_token: Token | None
    def __init__(
        self,
        text: str,
        line_ctr: LineCounter | None = None,
        last_token: Token | None = None,
    ) -> None: ...
    def __eq__(self, other): ...
    def __copy__(self): ...

class LexerThread:
    lexer: Incomplete
    state: Incomplete
    def __init__(self, lexer: Lexer, lexer_state: LexerState) -> None: ...
    @classmethod
    def from_text(cls, lexer: Lexer, text: str) -> LexerThread: ...
    def lex(self, parser_state): ...
    def __copy__(self): ...

class Lexer(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def lex(self, lexer_state: LexerState, parser_state: Any) -> Iterator[Token]: ...
    def make_lexer_state(self, text): ...

class AbstractBasicLexer(Lexer, metaclass=abc.ABCMeta):
    terminals_by_name: dict[str, TerminalDef]
    @abstractmethod
    def __init__(self, conf: LexerConf, comparator: Incomplete | None = None): ...
    @abstractmethod
    def next_token(self, lex_state: LexerState, parser_state: Any = None) -> Token: ...
    def lex(self, state: LexerState, parser_state: Any) -> Iterator[Token]: ...

class BasicLexer(AbstractBasicLexer):
    terminals: Collection[TerminalDef]
    ignore_types: frozenset[str]
    newline_types: frozenset[str]
    user_callbacks: dict[str, _Callback]
    callback: dict[str, _Callback]
    re: ModuleType
    g_regex_flags: Incomplete
    use_bytes: Incomplete
    terminals_by_name: Incomplete
    def __init__(
        self, conf: LexerConf, comparator: Incomplete | None = None
    ) -> None: ...
    @property
    def scanner(self): ...
    def match(self, text, pos): ...
    def next_token(self, lex_state: LexerState, parser_state: Any = None) -> Token: ...

class ContextualLexer(Lexer):
    lexers: dict[int, AbstractBasicLexer]
    root_lexer: AbstractBasicLexer
    BasicLexer: type[AbstractBasicLexer]
    def __init__(
        self,
        conf: LexerConf,
        states: dict[int, Collection[str]],
        always_accept: Collection[str] = (),
    ) -> None: ...
    def lex(
        self, lexer_state: LexerState, parser_state: ParserState
    ) -> Iterator[Token]: ...

ParserCallbacks = dict[str, Callable]

class LexerConf(Serialize):
    __serialize_fields__: Incomplete
    __serialize_namespace__: Incomplete
    terminals: Collection[TerminalDef]
    re_module: ModuleType
    ignore: Collection[str]
    postlex: PostLex | None
    callbacks: dict[str, _LexerCallback]
    g_regex_flags: int
    skip_validation: bool
    use_bytes: bool
    lexer_type: _LexerArgType | None
    strict: bool
    terminals_by_name: Incomplete
    def __init__(
        self,
        terminals: Collection[TerminalDef],
        re_module: ModuleType,
        ignore: Collection[str] = (),
        postlex: PostLex | None = None,
        callbacks: dict[str, _LexerCallback] | None = None,
        g_regex_flags: int = 0,
        skip_validation: bool = False,
        use_bytes: bool = False,
        strict: bool = False,
    ) -> None: ...
    def __deepcopy__(self, memo: Incomplete | None = None): ...

class ParserConf(Serialize):
    __serialize_fields__: Incomplete
    rules: list["Rule"]
    callbacks: ParserCallbacks
    start: list[str]
    parser_type: _ParserArgType
    def __init__(
        self, rules: list["Rule"], callbacks: ParserCallbacks, start: list[str]
    ) -> None: ...

class ExpandSingleChild:
    node_builder: Incomplete
    def __init__(self, node_builder) -> None: ...
    def __call__(self, children): ...

class PropagatePositions:
    node_builder: Incomplete
    node_filter: Incomplete
    def __init__(self, node_builder, node_filter: Incomplete | None = None) -> None: ...
    def __call__(self, children): ...

def make_propagate_positions(option): ...

class ChildFilter:
    node_builder: Incomplete
    to_include: Incomplete
    append_none: Incomplete
    def __init__(self, to_include, append_none, node_builder) -> None: ...
    def __call__(self, children): ...

class ChildFilterLALR(ChildFilter):
    def __call__(self, children): ...

class ChildFilterLALR_NoPlaceholders(ChildFilter):
    node_builder: Incomplete
    to_include: Incomplete
    def __init__(self, to_include, node_builder) -> None: ...
    def __call__(self, children): ...

def maybe_create_child_filter(
    expansion, keep_all_tokens, ambiguous, _empty_indices: list[bool]
): ...

class AmbiguousExpander:
    node_builder: Incomplete
    tree_class: Incomplete
    to_expand: Incomplete
    def __init__(self, to_expand, tree_class, node_builder) -> None: ...
    def __call__(self, children): ...

def maybe_create_ambiguous_expander(tree_class, expansion, keep_all_tokens): ...

class AmbiguousIntermediateExpander:
    node_builder: Incomplete
    tree_class: Incomplete
    def __init__(self, tree_class, node_builder) -> None: ...
    def __call__(self, children): ...

def inplace_transformer(func): ...
def apply_visit_wrapper(func, name, wrapper): ...

class ParseTreeBuilder:
    tree_class: Incomplete
    propagate_positions: Incomplete
    ambiguous: Incomplete
    maybe_placeholders: Incomplete
    rule_builders: Incomplete
    def __init__(
        self,
        rules,
        tree_class,
        propagate_positions: bool = False,
        ambiguous: bool = False,
        maybe_placeholders: bool = False,
    ) -> None: ...
    def create_callback(self, transformer: Incomplete | None = None): ...

class Action:
    name: Incomplete
    def __init__(self, name) -> None: ...

Shift: Incomplete
Reduce: Incomplete
StateT = TypeVar("StateT")

class ParseTableBase(Generic[StateT]):
    states: dict[StateT, dict[str, tuple]]
    start_states: dict[str, StateT]
    end_states: dict[str, StateT]
    def __init__(self, states, start_states, end_states) -> None: ...
    def serialize(self, memo): ...
    @classmethod
    def deserialize(cls, data, memo): ...

class ParseTable(ParseTableBase["State"]): ...

class IntParseTable(ParseTableBase[int]):
    @classmethod
    def from_ParseTable(cls, parse_table: ParseTable): ...

class ParseConf(Generic[StateT]):
    parse_table: ParseTableBase[StateT]
    callbacks: ParserCallbacks
    start: str
    start_state: StateT
    end_state: StateT
    states: dict[StateT, dict[str, tuple]]
    def __init__(
        self,
        parse_table: ParseTableBase[StateT],
        callbacks: ParserCallbacks,
        start: str,
    ) -> None: ...

class ParserState(Generic[StateT]):
    parse_conf: ParseConf[StateT]
    lexer: LexerThread
    state_stack: list[StateT]
    value_stack: list
    def __init__(
        self,
        parse_conf: ParseConf[StateT],
        lexer: LexerThread,
        state_stack: Incomplete | None = None,
        value_stack: Incomplete | None = None,
    ) -> None: ...
    @property
    def position(self) -> StateT: ...
    def __eq__(self, other) -> bool: ...
    def __copy__(self): ...
    def copy(self) -> ParserState[StateT]: ...
    def feed_token(self, token: Token, is_end: bool = False) -> Any: ...

class LALR_Parser(Serialize):
    parser_conf: Incomplete
    parser: Incomplete
    def __init__(
        self, parser_conf: ParserConf, debug: bool = False, strict: bool = False
    ) -> None: ...
    @classmethod
    def deserialize(cls, data, memo, callbacks, debug: bool = False): ...
    def serialize(self, memo: Any = None) -> dict[str, Any]: ...
    def parse_interactive(self, lexer: LexerThread, start: str): ...
    def parse(self, lexer, start, on_error: Incomplete | None = None): ...

class _Parser:
    parse_table: ParseTableBase
    callbacks: ParserCallbacks
    debug: bool
    def __init__(
        self,
        parse_table: ParseTableBase,
        callbacks: ParserCallbacks,
        debug: bool = False,
    ) -> None: ...
    def parse(
        self,
        lexer: LexerThread,
        start: str,
        value_stack: Incomplete | None = None,
        state_stack: Incomplete | None = None,
        start_interactive: bool = False,
    ): ...
    def parse_from_state(self, state: ParserState, last_token: Token | None = None): ...

class InteractiveParser:
    parser: Incomplete
    parser_state: Incomplete
    lexer_thread: Incomplete
    result: Incomplete
    def __init__(self, parser, parser_state, lexer_thread: LexerThread) -> None: ...
    @property
    def lexer_state(self) -> LexerThread: ...
    def feed_token(self, token: Token): ...
    def iter_parse(self) -> Iterator[Token]: ...
    def exhaust_lexer(self) -> list[Token]: ...
    def feed_eof(self, last_token: Incomplete | None = None): ...
    def __copy__(self): ...
    def copy(self): ...
    def __eq__(self, other): ...
    def as_immutable(self): ...
    def pretty(self): ...
    def choices(self): ...
    def accepts(self): ...
    def resume_parse(self): ...

class ImmutableInteractiveParser(InteractiveParser):
    result: Incomplete
    def __hash__(self): ...
    def feed_token(self, token): ...
    def exhaust_lexer(self): ...
    def as_mutable(self): ...

class ParsingFrontend(Serialize):
    __serialize_fields__: Incomplete
    lexer_conf: LexerConf
    parser_conf: ParserConf
    options: Any
    parser: Incomplete
    skip_lexer: bool
    lexer: Incomplete
    def __init__(
        self,
        lexer_conf: LexerConf,
        parser_conf: ParserConf,
        options,
        parser: Incomplete | None = None,
    ) -> None: ...
    def parse(
        self,
        text: str,
        start: Incomplete | None = None,
        on_error: Incomplete | None = None,
    ): ...
    def parse_interactive(
        self, text: str | None = None, start: Incomplete | None = None
    ): ...

class PostLexConnector:
    lexer: Incomplete
    postlexer: Incomplete
    def __init__(self, lexer, postlexer) -> None: ...
    def lex(self, lexer_state, parser_state): ...

def create_basic_lexer(lexer_conf, parser, postlex, options) -> BasicLexer: ...
def create_contextual_lexer(
    lexer_conf: LexerConf, parser, postlex, options
) -> ContextualLexer: ...
def create_lalr_parser(
    lexer_conf: LexerConf, parser_conf: ParserConf, options: Incomplete | None = None
) -> LALR_Parser: ...

class PostLex(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def process(self, stream: Iterator[Token]) -> Iterator[Token]: ...
    always_accept: Iterable[str]

class LarkOptions(Serialize):
    start: list[str]
    debug: bool
    strict: bool
    transformer: Transformer | None
    propagate_positions: bool | str
    maybe_placeholders: bool
    cache: bool | str
    regex: bool
    g_regex_flags: int
    keep_all_tokens: bool
    tree_class: Callable[[str, list], Any] | None
    parser: _ParserArgType
    lexer: _LexerArgType
    ambiguity: Literal["auto", "resolve", "explicit", "forest"]
    postlex: PostLex | None
    priority: Literal["auto", "normal", "invert"] | None
    lexer_callbacks: dict[str, Callable[[Token], Token]]
    use_bytes: bool
    ordered_sets: bool
    edit_terminals: Callable[[TerminalDef], TerminalDef] | None
    import_paths: list[
        str | Callable[[None | str | PackageResource, str], tuple[str, str]]
    ]
    source_path: str | None
    OPTIONS_DOC: str
    def __init__(self, options_dict: dict[str, Any]) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: str) -> None: ...
    def serialize(self, memo: Incomplete | None = None) -> dict[str, Any]: ...
    @classmethod
    def deserialize(
        cls, data: dict[str, Any], memo: dict[int, TerminalDef | Rule]
    ) -> LarkOptions: ...

class Lark(Serialize):
    source_path: str
    source_grammar: str
    grammar: Grammar
    options: LarkOptions
    lexer: Lexer
    parser: ParsingFrontend
    terminals: Collection[TerminalDef]
    lexer_conf: Incomplete
    def __init__(self, grammar: Grammar | str | IO[str], **options) -> None: ...
    __serialize_fields__: Incomplete
    def save(self, f, exclude_options: Collection[str] = ()) -> None: ...
    @classmethod
    def load(cls, f) -> _T: ...
    @classmethod
    def open(
        cls, grammar_filename: str, rel_to: str | None = None, **options
    ) -> _T: ...
    @classmethod
    def open_from_package(
        cls,
        package: str,
        grammar_path: str,
        search_paths: Sequence[str] = [""],
        **options
    ) -> _T: ...
    def lex(self, text: str, dont_ignore: bool = False) -> Iterator[Token]: ...
    def get_terminal(self, name: str) -> TerminalDef: ...
    def parse_interactive(
        self, text: str | None = None, start: str | None = None
    ) -> InteractiveParser: ...
    def parse(
        self,
        text: str,
        start: str | None = None,
        on_error: Callable[[UnexpectedInput], bool] | None = None,
    ) -> ParseTree: ...

class DedentError(LarkError): ...

class Indenter(PostLex, ABC, metaclass=abc.ABCMeta):
    paren_level: int
    indent_level: list[int]
    def __init__(self) -> None: ...
    def handle_NL(self, token: Token) -> Iterator[Token]: ...
    def process(self, stream): ...
    @property
    def always_accept(self): ...
    @property
    @abstractmethod
    def NL_type(self) -> str: ...
    @property
    @abstractmethod
    def OPEN_PAREN_types(self) -> list[str]: ...
    @property
    @abstractmethod
    def CLOSE_PAREN_types(self) -> list[str]: ...
    @property
    @abstractmethod
    def INDENT_type(self) -> str: ...
    @property
    @abstractmethod
    def DEDENT_type(self) -> str: ...
    @property
    @abstractmethod
    def tab_len(self) -> int: ...

class PythonIndenter(Indenter):
    NL_type: str
    OPEN_PAREN_types: Incomplete
    CLOSE_PAREN_types: Incomplete
    INDENT_type: str
    DEDENT_type: str
    tab_len: int

DATA: bytes
MEMO: bytes

def Lark_StandAlone(**kwargs): ...
