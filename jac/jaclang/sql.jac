import from uuid { UUID }

class SqlError(ValueError) {}

obj SqlBool {}
obj SqlInt64 {}
obj SqlFloat64 {}
obj SqlText {}
obj SqlUUID {}
obj Nullable[T] {}
obj Many {}
obj AtMostOne {}
obj ExactlyOne {}

obj SqlValue {
    def __setattr__(name: str, value: any);
    def __delattr__(name: str);
}

obj DataType(SqlValue) {
    has name: str,
        nullable: bool = False;

    def postinit;
}

obj SqlType[T](SqlValue) {
    has data: DataType;
}

obj FieldDef(SqlValue) {
    has name: str,
        dtype: DataType;
}

obj Field[T](FieldDef) {}

obj Schema(SqlValue) {
    has fields: tuple[FieldDef, ...];

    def postinit;
    def find(name: str) -> FieldDef;
}

obj RelationNode(SqlValue) {
    has cardinality: str;
    has schema: Schema {
        getter {
            raise SqlError('Unknown relation schema');
        }
    }
}

obj Source(SqlValue) {
    has alias: str;
    has schema: Schema {
        getter {
            raise SqlError('Unknown source schema');
        }
    }

    def ref -> Source;
    def col[T](key: Field[T]) -> ScalarExpr[T];
}

obj Table(Source) {
    has declared_schema: Schema,
        name: tuple[str, ...];

    has schema: Schema {
        getter {
            return self.declared_schema;
        }
    }
}

obj Derived(Source) {
    has query: RelationNode;
    has schema: Schema {
        getter {
            return self.query.schema;
        }
    }
}

obj CteBinding(SqlValue) {
    has _definition: RelationNode | None = None,
        _recursive: bool = False;

    has definition: RelationNode | None {
        getter {
            return self._definition;
        }
    }

    has recursive: bool {
        getter {
            return self._recursive;
        }
    }

    def __setattr__(name: str, value: any);
    def bind(query: RelationNode, recursive: bool);
}

obj Cte(Source) {
    has binding: CteBinding,
        declared_schema: Schema | None = None;

    has definition: RelationNode | None {
        getter {
            return self.binding.definition;
        }
    }

    has recursive: bool {
        getter {
            return self.binding.recursive;
        }
    }

    has schema: Schema {
        getter {
            if self.declared_schema is not None {
                return self.declared_schema;
            }
            if self.definition is not None {
                return self.definition.schema;
            }
            raise SqlError('CTE reference has no schema');
        }
    }
}

obj CteUse(Source) {
    has target: Cte;
    has schema: Schema {
        getter {
            return self.target.schema;
        }
    }
}

obj ExprNode(SqlValue) {
    has dtype: DataType;
}

obj ColumnNode(ExprNode) {
    has source: Source,
        name: str;
}

obj ParamNode(ExprNode) {
    has value: bool | int | float | str | UUID | None;
}

obj BinaryNode(ExprNode) {
    has op: str,
        left: ExprNode,
        right: ExprNode;
}

obj BoolNode(ExprNode) {
    has op: str,
        terms: tuple[ExprNode, ...];
}

obj UnaryNode(ExprNode) {
    has op: str,
        term: ExprNode;
}

obj CastNode(ExprNode) {
    has term: ExprNode;
}

obj AggregateNode(ExprNode) {
    has op: str,
        term: ExprNode | None;
}

obj CoalesceNode(ExprNode) {
    has term: ExprNode,
        fallback: ExprNode;
}

obj ScalarNode(ExprNode) {
    has query: RelationNode,
        require_one: bool;
}

obj ExistsNode(ExprNode) {
    has query: RelationNode;
}

obj ScalarExpr[T](SqlValue) {
    has ast: ExprNode;
}

obj ProjectionDef(SqlValue) {
    has field: FieldDef,
        expr: ExprNode;
}

obj Projection[T](ProjectionDef) {
    def key -> Field[T];
}

obj Order(SqlValue) {
    has expr: ExprNode,
        descending: bool;
}

obj Join(SqlValue) {
    has source: Source,
        condition: ExprNode;
}

obj SelectNode(RelationNode) {
    has projections: tuple[ProjectionDef, ...],
        source: Source | None,
        joins: tuple[Join, ...],
        predicate: ExprNode | None,
        groups: tuple[ExprNode, ...],
        having: ExprNode | None,
        ordering: tuple[Order, ...],
        limit: int | None;

    has schema: Schema {
        getter {
            return Schema(tuple(p.field for p in self.projections));
        }
    }
}

obj UnionNode(RelationNode) {
    has left: RelationNode,
        right: RelationNode,
        keep_duplicates: bool;

    has schema: Schema {
        getter {
            return self.left.schema;
        }
    }
}

obj Relation[R, C](SqlValue) {
    has ast: RelationNode;

    def as_source -> Source;
}

obj Command {}

obj CompiledSQL {
    has sql: str,
        params: dict[str, bool | int | float | str | UUID | None];
}


def same_type(a: DataType, b: DataType) -> bool;


def bool_type -> SqlType[SqlBool];

def int64_type -> SqlType[SqlInt64];

def float64_type -> SqlType[SqlFloat64];

def text_type -> SqlType[SqlText];

def uuid_type -> SqlType[SqlUUID];

def nullable[T](dtype: SqlType[T]) -> SqlType[Nullable[T]];

def field[T](name: str, dtype: SqlType[T]) -> Field[T];

def table(
    name: str, fields: list[FieldDef], alias: str = '', namespace: str | None = None
) -> Source;

def param[T](
    dtype: SqlType[T], value: bool | int | float | str | UUID | None
) -> ScalarExpr[T];

def int64(value: int) -> ScalarExpr[SqlInt64];

def text(value: str) -> ScalarExpr[SqlText];

def boolean(value: bool) -> ScalarExpr[SqlBool];

def uuid(value: UUID) -> ScalarExpr[SqlUUID];

def validate_value(
    dtype: DataType, value: bool | int | float | str | UUID | None
) -> None;

def _compare[T](
    left: ScalarExpr[T], right: ScalarExpr[T], op: str
) -> ScalarExpr[SqlBool];

def eq[T](left: ScalarExpr[T], right: ScalarExpr[T]) -> ScalarExpr[SqlBool];

def gt[T](left: ScalarExpr[T], right: ScalarExpr[T]) -> ScalarExpr[SqlBool];

def eq_nullable[T](
    left: ScalarExpr[Nullable[T]], right: ScalarExpr[Nullable[T]]
) -> ScalarExpr[Nullable[SqlBool]];

def add(
    left: ScalarExpr[SqlInt64], right: ScalarExpr[SqlInt64]
) -> ScalarExpr[SqlInt64];

def and_(terms: list[ScalarExpr[SqlBool]]) -> ScalarExpr[SqlBool];

def is_null[T](term: ScalarExpr[Nullable[T]]) -> ScalarExpr[SqlBool];

def cast[T, U](term: ScalarExpr[T], dtype: SqlType[U]) -> ScalarExpr[U];

def count -> ScalarExpr[SqlInt64];

def sum_(term: ScalarExpr[SqlFloat64]) -> ScalarExpr[Nullable[SqlFloat64]];

def coalesce[T](
    term: ScalarExpr[Nullable[T]], fallback: ScalarExpr[T]
) -> ScalarExpr[T];

def named[T](name: str, expr: ScalarExpr[T]) -> Projection[T];

def asc[T](expr: ScalarExpr[T]) -> Order;

def desc[T](expr: ScalarExpr[T]) -> Order;

def inner_join(
    source: Source, on: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]]
) -> Join;

def select(
    projections: list[ProjectionDef],
    source: Source | None = None,
    joins: list[Join] = [],
    where: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]] | None = None,
    group_by: list[ExprNode] = [],
    having: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]] | None = None,
    order_by: list[Order] = [],
    limit: int | None = None
) -> Relation[Schema, Many];

def limit_one[R, C](query: Relation[R, C]) -> Relation[R, AtMostOne];

def aggregate(
    projections: list[ProjectionDef],
    source: Source | None = None,
    where: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]] | None = None
) -> Relation[Schema, ExactlyOne];

def scalar[R, T](
    query: Relation[R, AtMostOne] | Relation[R, ExactlyOne], key: Field[T]
) -> ScalarExpr[Nullable[T]];

def scalar_one[R, T](query: Relation[R, ExactlyOne], key: Field[T]) -> ScalarExpr[T];

def exists[R, C](query: Relation[R, C]) -> ScalarExpr[SqlBool];

def union_all[R, C, D](
    left: Relation[R, C], right: Relation[R, D]
) -> Relation[R, Many];

def cte[R, C](query: Relation[R, C]) -> Cte;

def cte_ref(fields: list[FieldDef]) -> Cte;

def define_cte[R, C](
    reference: Cte, query: Relation[R, C], recursive: bool = False
) -> Cte;


obj Checked {
    has free: set[str],
        aggregate: bool = False;
}

obj QueryFacts {
    has external: set[str];
}

obj ValidatedQuery {
    has query: RelationNode,
        ctes: tuple[Cte, ...],
        aliases: dict[int, str],
        cte_names: dict[int, str];
}


def validate_identifier(name: str);

def quote_identifier(name: str) -> str;


def _key(source: Source, name: str) -> str;

def _schema_equal(a: Schema, b: Schema, names: bool = True) -> bool;

def validate_union(ast: UnionNode);

obj QueryGraph {
    has ctes: list[Cte] = [],
        physical_names: set[str] = set(),
        explicit_aliases: set[str] = set(),
        seen_sources: set[int] = set(),
        seen_queries: set[int] = set(),
        active_queries: set[int] = set(),
        seen_expressions: set[int] = set();

    def visit_source(src: Source) -> None;
    def collect(query: RelationNode);
    def visit_expr(expr: ExprNode) -> None;
    def visit_query(query: RelationNode) -> None;
}


obj QueryValidator {
    has active_queries: set[int] = set(),
        aliases: dict[int, str] = {},
        cte_names: dict[int, str] = {},
        used_names: set[str] = set(),
        ordered_ctes: list[Cte] = [],
        cte_states: dict[int, int] = {},
        alias_counter: int = 0,
        cte_counter: int = 0;

    def fresh_name(prefix: str) -> str;
    def alias_for(src: Source) -> str;
    def order_cte(reference: Cte) -> None;
    def analyze[R, C](query: Relation[R, C]) -> ValidatedQuery;
    def source(src: Source, ctes: list[Cte]) -> None;
    def expr(
        ast: ExprNode, scope: list[Source], local: list[Source], ctes: list[Cte]
    ) -> Checked;

    def query(ast: RelationNode, outer: list[Source], ctes: list[Cte]) -> QueryFacts;
    def query_body(
        ast: RelationNode, outer: list[Source], ctes: list[Cte]
    ) -> QueryFacts;

    def select_sql(
        ast: SelectNode, outer: list[Source], ctes: list[Cte]
    ) -> QueryFacts;
}


obj PostgresRenderer {
    has params: dict[str, bool | int | float | str | UUID | None] = {},
        parameter_ids: dict[int, str] = {},
        aliases: dict[int, str] = {},
        cte_names: dict[int, str] = {};

    def alias_for(src: Source) -> str;
    def render(plan: ValidatedQuery) -> CompiledSQL;
    def source(src: Source) -> str;
    def expr(ast: ExprNode) -> str;
    def query(ast: RelationNode) -> str;
}


def compile_sql[R, C](query: Relation[R, C]) -> CompiledSQL;


def validate_recursive_step(ref: Cte, step: SelectNode);
