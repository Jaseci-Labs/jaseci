"""Typed, dependency-free SQL AST and PostgreSQL renderer. Portable as one file."""

import from uuid { UUID }

"""Dependency-free SQL types and structural nodes. No graph/runtime imports."""
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

"""SQL values are immutable; use constructors to build a changed query."""
obj SqlValue {
    def __setattr__(name: str, value: any) -> None {
        if name in self.__dict__ {
            raise SqlError('SQL values are immutable; construct a new value');
        }
        object.__setattr__(
            self, name, tuple(value) if isinstance(value, list) else value
        );
    }

    def __delattr__(name: str) -> None {
        raise SqlError('SQL values are immutable; construct a new value');
    }
}

obj DataType(SqlValue) {
    has name: str,
        nullable: bool = False;

    def postinit {
        if self.name not in ('boolean', 'bigint', 'double precision', 'text', 'uuid') {
            raise SqlError(f"Unsupported SQL type: {self.name}");
        }
    }
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

    def postinit {
        names: set[str] = set();
        for f in self.fields {
            if not f.name or '\x00' in f.name or f.name in names {
                raise SqlError(f"Empty, NUL or duplicate field name: {f.name}");
            }
            names.add(f.name);
        }
        if not self.fields {
            raise SqlError("A row schema must have at least one field");
        }
    }

    def find(name: str) -> FieldDef {
        for f in self.fields {
            if f.name == name {
                return f;
            }
        }
        raise SqlError(f"Unknown column: {name}");
    }
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

    def ref -> Source {
        if isinstance(self, Table) {
            return Table(declared_schema=self.schema, alias='', name=self.name);
        }
        if isinstance(self, Derived) {
            return Derived(alias='', query=self.query);
        }
        if isinstance(self, Cte) {
            return CteUse(alias='', target=self);
        }
        if isinstance(self, CteUse) {
            return CteUse(alias='', target=self.target);
        }
        raise SqlError('Unknown source binding');
    }

    def col[T](key: Field[T]) -> ScalarExpr[T] {
        actual = self.schema.find(key.name);
        if not same_type(actual.dtype, key.dtype) {
            raise SqlError(f"Column type mismatch: {key.name}");
        }
        return ScalarExpr(
            ast=ColumnNode(dtype=actual.dtype, source=self, name=key.name)
        );
    }
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

"""One explicit construction-time hole permits recursive references."""
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

    def __setattr__(name: str, value: any) -> None {
        if self.__dict__.get('_definition') is not None {
            raise SqlError('CTE reference is already defined');
        }
        object.__setattr__(self, name, value);
    }

    def bind(query: RelationNode, recursive: bool) -> None {
        if self._definition is not None {
            raise SqlError('CTE reference is already defined');
        }
        self._recursive = recursive;
        self._definition = query;
    }
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
    def key -> Field[T] {
        return Field(name=self.field.name, dtype=self.field.dtype);
    }
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

    def as_source -> Source {
        return Derived(alias='', query=self.ast);
    }
}

obj Command {}

obj CompiledSQL {
    has sql: str,
        params: dict[str, bool | int | float | str | UUID | None];
}


def same_type(a: DataType, b: DataType) -> bool {
    return a.name == b.name and a.nullable == b.nullable;
}


"""Typed construction API. Schema/cardinality checks complement Jac signatures."""
def bool_type -> SqlType[SqlBool] {
    return SqlType(DataType('boolean'));
}

def int64_type -> SqlType[SqlInt64] {
    return SqlType(DataType('bigint'));
}

def float64_type -> SqlType[SqlFloat64] {
    return SqlType(DataType('double precision'));
}

def text_type -> SqlType[SqlText] {
    return SqlType(DataType('text'));
}

def uuid_type -> SqlType[SqlUUID] {
    return SqlType(DataType('uuid'));
}

def nullable[T](dtype: SqlType[T]) -> SqlType[Nullable[T]] {
    if dtype.data.nullable {
        raise SqlError('Type is already nullable');
    }
    return SqlType(DataType(dtype.data.name, True));
}

def field[T](name: str, dtype: SqlType[T]) -> Field[T] {
    return Field(name=name, dtype=dtype.data);
}

def table(
    name: str, fields: list[FieldDef], alias: str = '', namespace: str | None = None
) -> Source {
    parts = [name] if namespace is None else [namespace, name];
    return Table(declared_schema=Schema(tuple(fields)), alias=alias, name=tuple(parts));
}

def param[T](
    dtype: SqlType[T], value: bool | int | float | str | UUID | None
) -> ScalarExpr[T] {
    validate_value(dtype.data, value);
    return ScalarExpr(ParamNode(dtype=dtype.data, value=value));
}

def int64(value: int) -> ScalarExpr[SqlInt64] {
    return param(int64_type(), value);
}

def text(value: str) -> ScalarExpr[SqlText] {
    return param(text_type(), value);
}

def boolean(value: bool) -> ScalarExpr[SqlBool] {
    return param(bool_type(), value);
}

def uuid(value: UUID) -> ScalarExpr[SqlUUID] {
    return param(uuid_type(), value);
}

def validate_value(
    dtype: DataType, value: bool | int | float | str | UUID | None
) -> None {
    if value is None {
        if not dtype.nullable {
            raise SqlError('NULL requires a nullable SQL type');
        }
        return;
    }
    valid = False;
    if dtype.name == 'boolean' {
        valid = type(value) is bool;
    } elif dtype.name == 'bigint' {
        valid = type(value) is int;
        if valid and (value < -9223372036854775808 or value > 9223372036854775807) {
            raise SqlError('Value is outside signed int64');
        }
    } elif dtype.name == 'double precision' {
        valid = type(value) is float;
    } elif dtype.name == 'text' {
        valid = type(value) is str;
    } elif dtype.name == 'uuid' {
        valid = isinstance(value, UUID);
    }
    if not valid {
        raise SqlError(f'Invalid parameter value for {dtype.name}');
    }
}

def _compare[T](
    left: ScalarExpr[T], right: ScalarExpr[T], op: str
) -> ScalarExpr[SqlBool] {
    if not same_type(left.ast.dtype, right.ast.dtype) or left.ast.dtype.nullable {
        raise SqlError(
            'Comparison requires identical non-null SQL types; use eq_nullable for NULL'
        );
    }
    return ScalarExpr(
        BinaryNode(dtype=DataType('boolean'), op=op, left=left.ast, right=right.ast)
    );
}

def eq[T](left: ScalarExpr[T], right: ScalarExpr[T]) -> ScalarExpr[SqlBool] {
    return _compare(left, right, '=');
}

def gt[T](left: ScalarExpr[T], right: ScalarExpr[T]) -> ScalarExpr[SqlBool] {
    if left.ast.dtype.name not in ('bigint', 'double precision', 'text') {
        raise SqlError('Type has no supported ordering');
    }
    return _compare(left, right, '>');
}

def eq_nullable[T](
    left: ScalarExpr[Nullable[T]], right: ScalarExpr[Nullable[T]]
) -> ScalarExpr[Nullable[SqlBool]] {
    if not same_type(left.ast.dtype, right.ast.dtype) or not left.ast.dtype.nullable {
        raise SqlError('eq_nullable requires identical nullable types');
    }
    return ScalarExpr(
        BinaryNode(
            dtype=DataType('boolean', True), op='=', left=left.ast, right=right.ast
        )
    );
}

def add(
    left: ScalarExpr[SqlInt64], right: ScalarExpr[SqlInt64]
) -> ScalarExpr[SqlInt64] {
    for term in [left.ast, right.ast] {
        if term.dtype.name != 'bigint' or term.dtype.nullable {
            raise SqlError('add requires non-null int64 operands');
        }
    }
    return ScalarExpr(
        BinaryNode(dtype=DataType('bigint'), op='+', left=left.ast, right=right.ast)
    );
}

def and_(terms: list[ScalarExpr[SqlBool]]) -> ScalarExpr[SqlBool] {
    if not terms {
        raise SqlError('and_ requires at least one operand');
    }
    for term in terms {
        if term.ast.dtype.name != 'boolean' or term.ast.dtype.nullable {
            raise SqlError('and_ requires non-null boolean operands');
        }
    }
    return ScalarExpr(
        BoolNode(dtype=DataType('boolean'), op='AND', terms=tuple(t.ast for t in terms))
    );
}

def is_null[T](term: ScalarExpr[Nullable[T]]) -> ScalarExpr[SqlBool] {
    if not term.ast.dtype.nullable {
        raise SqlError('is_null expects a nullable expression');
    }
    return ScalarExpr(
        UnaryNode(dtype=DataType('boolean'), op='IS NULL', term=term.ast)
    );
}

def cast[T, U](term: ScalarExpr[T], dtype: SqlType[U]) -> ScalarExpr[U] {
    if term.ast.dtype.nullable and not dtype.data.nullable {
        raise SqlError('CAST does not remove NULL');
    }
    return ScalarExpr(CastNode(dtype=dtype.data, term=term.ast));
}

def count -> ScalarExpr[SqlInt64] {
    return ScalarExpr(AggregateNode(dtype=DataType('bigint'), op='COUNT', term=None));
}

def sum_(term: ScalarExpr[SqlFloat64]) -> ScalarExpr[Nullable[SqlFloat64]] {
    if term.ast.dtype.name != 'double precision' or term.ast.dtype.nullable {
        raise SqlError('sum_ expects float64');
    }
    return ScalarExpr(
        AggregateNode(dtype=DataType('double precision', True), op='SUM', term=term.ast)
    );
}

def coalesce[T](
    term: ScalarExpr[Nullable[T]], fallback: ScalarExpr[T]
) -> ScalarExpr[T] {
    a = term.ast.dtype;
    b = fallback.ast.dtype;
    if not a.nullable or b.nullable or a.name != b.name {
        raise SqlError('Invalid COALESCE types');
    }
    return ScalarExpr(CoalesceNode(dtype=b, term=term.ast, fallback=fallback.ast));
}

def named[T](name: str, expr: ScalarExpr[T]) -> Projection[T] {
    if not isinstance(expr, ScalarExpr) {
        raise SqlError('Projection requires a scalar expression');
    }
    return Projection(field=Field(name=name, dtype=expr.ast.dtype), expr=expr.ast);
}

def asc[T](expr: ScalarExpr[T]) -> Order {
    return Order(expr=expr.ast, descending=False);
}

def desc[T](expr: ScalarExpr[T]) -> Order {
    return Order(expr=expr.ast, descending=True);
}

def inner_join(
    source: Source, on: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]]
) -> Join {
    if on.ast.dtype.name != 'boolean' {
        raise SqlError('JOIN ON requires a boolean');
    }
    return Join(source=source, condition=on.ast);
}

def select(
    projections: list[ProjectionDef],
    source: Source | None = None,
    joins: list[Join] = [],
    where: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]] | None = None,
    group_by: list[ExprNode] = [],
    having: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]] | None = None,
    order_by: list[Order] = [],
    limit: int | None = None
) -> Relation[Schema, Many] {
    if where is not None and where.ast.dtype.name != 'boolean' {
        raise SqlError('WHERE requires a boolean');
    }
    if having is not None and having.ast.dtype.name != 'boolean' {
        raise SqlError('HAVING requires a boolean');
    }
    if limit is not None and (type(limit) is not int or limit < 0) {
        raise SqlError('LIMIT must be a non-negative integer');
    }
    return Relation(
        SelectNode(
            cardinality='many',
            projections=tuple(projections),
            source=source,
            joins=tuple(joins),
            predicate=where.ast if where is not None else None,
            groups=tuple(group_by),
            having=having.ast if having is not None else None,
            ordering=tuple(order_by),
            limit=limit
        )
    );
}

def limit_one[R, C](query: Relation[R, C]) -> Relation[R, AtMostOne] {
    if not isinstance(query.ast, SelectNode) {
        raise SqlError('limit_one requires a SELECT');
    }
    q = query.ast;
    ast = SelectNode(
        cardinality='at_most_one',
        projections=q.projections,
        source=q.source,
        joins=q.joins,
        predicate=q.predicate,
        groups=q.groups,
        having=q.having,
        ordering=q.ordering,
        limit=1
    );
    return Relation(ast);
}

def aggregate(
    projections: list[ProjectionDef],
    source: Source | None = None,
    where: ScalarExpr[SqlBool] | ScalarExpr[Nullable[SqlBool]] | None = None
) -> Relation[Schema, ExactlyOne] {
    q = select(projections, source=source, where=where);
    ast = q.ast;
    if not isinstance(ast, SelectNode) {
        raise SqlError('Aggregate requires a SELECT');
    }
    return Relation(
        SelectNode(
            cardinality='exactly_one_aggregate',
            projections=ast.projections,
            source=ast.source,
            joins=ast.joins,
            predicate=ast.predicate,
            groups=ast.groups,
            having=ast.having,
            ordering=ast.ordering,
            limit=ast.limit
        )
    );
}

def scalar[R, T](
    query: Relation[R, AtMostOne] | Relation[R, ExactlyOne], key: Field[T]
) -> ScalarExpr[Nullable[T]] {
    q = query.ast;
    if len(q.schema.fields) != 1
        or q.cardinality not in ('at_most_one', 'exactly_one_aggregate') {
        raise SqlError(
            'Scalar subquery requires one column and a proven at-most-one row'
        );
    }
    actual = q.schema.find(key.name);
    if not same_type(actual.dtype, key.dtype) or actual.dtype.nullable {
        raise SqlError('Scalar key must match its non-null output column');
    }
    return ScalarExpr(
        ScalarNode(dtype=DataType(actual.dtype.name, True), query=q, require_one=False)
    );
}

def scalar_one[R, T](query: Relation[R, ExactlyOne], key: Field[T]) -> ScalarExpr[T] {
    q = query.ast;
    if q.cardinality != 'exactly_one_aggregate' or len(q.schema.fields) != 1 {
        raise SqlError('scalar_one requires exactly one row and column');
    }
    actual = q.schema.find(key.name);
    if not same_type(actual.dtype, key.dtype) {
        raise SqlError('Scalar output key mismatch');
    }
    return ScalarExpr(ScalarNode(dtype=actual.dtype, query=q, require_one=True));
}

def exists[R, C](query: Relation[R, C]) -> ScalarExpr[SqlBool] {
    return ScalarExpr(ExistsNode(dtype=DataType('boolean'), query=query.ast));
}

def union_all[R, C, D](
    left: Relation[R, C], right: Relation[R, D]
) -> Relation[R, Many] {
    a = left.ast.schema.fields;
    b = right.ast.schema.fields;
    if len(a) != len(b)
        or not all([same_type(x.dtype, y.dtype) for (x, y) in zip(a, b)]) {
        raise SqlError('UNION requires matching column counts, types and nullability');
    }
    return Relation(
        UnionNode(
            cardinality='many', left=left.ast, right=right.ast, keep_duplicates=True
        )
    );
}

def cte[R, C](query: Relation[R, C]) -> Cte {
    binding = CteBinding();
    binding.bind(query.ast, False);
    return Cte(binding=binding, alias='');
}

def cte_ref(fields: list[FieldDef]) -> Cte {
    return Cte(binding=CteBinding(), declared_schema=Schema(tuple(fields)), alias='');
}

def define_cte[R, C](
    reference: Cte, query: Relation[R, C], recursive: bool = False
) -> Cte {
    if reference.definition is not None {
        raise SqlError('CTE reference is already defined');
    }
    if not _schema_equal(reference.schema, query.ast.schema, False) {
        raise SqlError('CTE output schema differs from declared schema');
    }
    reference.binding.bind(query.ast, recursive);
    return reference;
}


"""Whole-query validation produces dependency facts and a resolved query plan."""
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


def validate_identifier(name: str) -> None {
    if not isinstance(name, str) or not name or '\x00' in name {
        raise SqlError('Identifier must be a nonempty string without NUL');
    }
}

def quote_identifier(name: str) -> str {
    validate_identifier(name);
    return '"' + name.replace('"', '""') + '"';
}


def _key(source: Source, name: str) -> str {
    return str(id(source)) + ':' + name;
}

def _schema_equal(a: Schema, b: Schema, names: bool = True) -> bool {
    if len(a.fields) != len(b.fields) {
        return False;
    }
    return all(
        [
            same_type(x.dtype, y.dtype) and (not names or x.name == y.name)
            for (x, y) in zip(a.fields, b.fields)
        ]
    );
}

def validate_union(ast: UnionNode) -> None {
    if not _schema_equal(ast.left.schema, ast.right.schema, False)
        or ast.cardinality != 'many' {
        raise SqlError('UNION schema/cardinality mismatch');
    }
}

obj QueryGraph {
    has ctes: list[Cte] = [],
        physical_names: set[str] = set(),
        explicit_aliases: set[str] = set(),
        seen_sources: set[int] = set(),
        seen_queries: set[int] = set(),
        active_queries: set[int] = set(),
        seen_expressions: set[int] = set();

    def visit_source(src: Source) -> None {
        identity = id(src);
        if identity in self.seen_sources {
            return;
        }
        self.seen_sources.add(identity);
        if isinstance(src, Table) {
            if src.name {
                self.physical_names.add(src.name[-1]);
            }
            if src.alias {
                self.explicit_aliases.add(src.alias);
            }
        } elif isinstance(src, Derived) {
            self.visit_query(src.query);
        } elif isinstance(src, CteUse) {
            self.visit_source(src.target);
        } elif isinstance(src, Cte) {
            self.ctes.append(src);
        } else {
            raise SqlError('Unknown SQL source ast');
        }
    }

    def collect(query: RelationNode) -> None {
        self.visit_query(query);
        index = 0;
        while index < len(self.ctes) {
            reference = self.ctes[index];
            if reference.definition is None {
                raise SqlError('CTE reference has no definition');
            }
            self.visit_query(reference.definition);
            index += 1;
        }
    }

    def visit_expr(expr: ExprNode) -> None {
        if not isinstance(expr, ExprNode) {
            raise SqlError('Expected a scalar SQL expression');
        }
        if id(expr) in self.seen_expressions {
            return;
        }
        self.seen_expressions.add(id(expr));
        if isinstance(expr, ColumnNode) {
            self.visit_source(expr.source);
        } elif isinstance(expr, (ScalarNode, ExistsNode)) {
            self.visit_query(expr.query);
        } elif isinstance(expr, BinaryNode) {
            self.visit_expr(expr.left);
            self.visit_expr(expr.right);
        } elif isinstance(expr, BoolNode) {
            for term in expr.terms {
                self.visit_expr(term);
            }
        } elif isinstance(expr, (UnaryNode, CastNode)) {
            self.visit_expr(expr.term);
        } elif isinstance(expr, AggregateNode) {
            if expr.term is not None {
                self.visit_expr(expr.term);
            }
        } elif isinstance(expr, CoalesceNode) {
            self.visit_expr(expr.term);
            self.visit_expr(expr.fallback);
        } elif not isinstance(expr, ParamNode) {
            raise SqlError('Unknown scalar SQL ast');
        }
    }

    def visit_query(query: RelationNode) -> None {
        if not isinstance(query, RelationNode) {
            raise SqlError('Expected a relation ast');
        }
        identity = id(query);
        if identity in self.active_queries {
            raise SqlError('Cyclic AST: use a recursive CTE reference');
        }
        if identity in self.seen_queries {
            return;
        }
        self.active_queries.add(identity);
        try {
            if isinstance(query, SelectNode) {
                if query.source is not None {
                    self.visit_source(query.source);
                }
                for join in query.joins {
                    self.visit_source(join.source);
                    self.visit_expr(join.condition);
                }
                for projection in query.projections {
                    self.visit_expr(projection.expr);
                }
                for expr in query.groups {
                    self.visit_expr(expr);
                }
                if query.predicate is not None {
                    self.visit_expr(query.predicate);
                }
                if query.having is not None {
                    self.visit_expr(query.having);
                }
                for ordering in query.ordering {
                    self.visit_expr(ordering.expr);
                }
            } elif isinstance(query, UnionNode) {
                self.visit_query(query.left);
                self.visit_query(query.right);
            } else {
                raise SqlError('Unknown relational ast');
            }
        } finally {
            self.active_queries.remove(identity);
        }
        self.seen_queries.add(identity);
    }
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

    def fresh_name(prefix: str) -> str {
        while True {
            index = self.cte_counter if prefix == '_cte' else self.alias_counter;
            if prefix == '_cte' {
                self.cte_counter += 1;
            } else {
                self.alias_counter += 1;
            }
            name = prefix + str(index);
            if name not in self.used_names {
                self.used_names.add(name);
                return name;
            }
        }
    }

    def alias_for(src: Source) -> str {
        if isinstance(src, Table) and src.alias {
            validate_identifier(src.alias);
            self.aliases[id(src)] = src.alias;
            return src.alias;
        }
        if src.alias {
            raise SqlError('Temporary source aliases are renderer-managed');
        }
        identity = id(src);
        if identity not in self.aliases {
            self.aliases[identity] = self.fresh_name('_t');
        }
        return self.aliases[identity];
    }

    def order_cte(reference: Cte) -> None {
        identity = id(reference);
        state = self.cte_states.get(identity, 0);
        if state == 2 {
            return;
        }
        if state == 1 {
            raise SqlError('Mutually dependent CTE definitions are unsupported');
        }
        if reference.definition is None {
            raise SqlError('CTE reference has no definition');
        }
        self.cte_states[identity] = 1;
        scan = QueryGraph();
        scan.visit_query(reference.definition);
        for dependency in scan.ctes {
            if dependency is reference {
                if not reference.recursive {
                    raise SqlError(
                        'Self-reference requires a recursive CTE definition'
                    );
                }
            } else {
                self.order_cte(dependency);
            }
        }
        self.cte_states[identity] = 2;
        self.ordered_ctes.append(reference);
    }

    def analyze[R, C](query: Relation[R, C]) -> ValidatedQuery {
        if not isinstance(query, Relation) {
            raise SqlError('Expected a relation, not a scalar or command');
        }
        self.active_queries = set();
        self.aliases = {};
        self.cte_names = {};
        self.used_names = set();
        self.ordered_ctes = [];
        self.cte_states = {};
        self.alias_counter = 0;
        self.cte_counter = 0;
        scan = QueryGraph();
        scan.collect(query.ast);
        self.used_names = scan.physical_names | scan.explicit_aliases;
        for reference in scan.ctes {
            self.order_cte(reference);
        }
        for reference in self.ordered_ctes {
            self.cte_names[id(reference)] = self.fresh_name('_cte');
        }
        available: list[Cte] = [];
        for reference in self.ordered_ctes {
            definition = reference.definition;
            if definition is None {
                raise SqlError('CTE reference has no definition');
            }
            if not _schema_equal(reference.schema, definition.schema, False) {
                raise SqlError('CTE output schema mismatch');
            }
            if reference.recursive {
                if not isinstance(definition, UnionNode)
                    or not definition.keep_duplicates {
                    raise SqlError('Recursive binding requires UNION ALL');
                }
                if not isinstance(definition.left, SelectNode)
                    or not isinstance(definition.right, SelectNode) {
                    raise SqlError(
                        'Recursive CTE requires a SELECT anchor and SELECT step'
                    );
                }
                validate_union(definition);
                validate_recursive_step(reference, definition.right);
                self.query(definition.left, [], available);
                self.query(definition.right, [], available + [reference]);
            } else {
                self.query(definition, [], available);
            }
            available.append(reference);
        }
        facts = self.query(query.ast, [], available);
        if facts.external {
            raise SqlError('Top-level query has unbound correlations');
        }
        return ValidatedQuery(
            query=query.ast,
            ctes=tuple(self.ordered_ctes),
            aliases=dict(self.aliases),
            cte_names=dict(self.cte_names)
        );
    }

    def source(src: Source, ctes: list[Cte]) -> None {
        Schema(tuple(src.schema.fields));
        self.alias_for(src);
        if isinstance(src, Table) {
            if not src.name {
                raise SqlError('Table needs a name');
            }
            for name in src.name {
                validate_identifier(name);
            }
            return;
        }
        if isinstance(src, Derived) {
            q = self.query(src.query, [], ctes);
            if q.external {
                raise SqlError('FROM subquery requires LATERAL for correlations');
            }
            return;
        }
        if isinstance(src, (Cte, CteUse)) {
            reference = src.target if isinstance(src, CteUse) else src;
            if not `any([x is reference for x in ctes]) {
                raise SqlError('CTE reference is outside scope');
            }
            return;
        }
        raise SqlError('Unknown SQL source ast');
    }

    def expr(
        ast: ExprNode, scope: list[Source], local: list[Source], ctes: list[Cte]
    ) -> Checked {
        if not isinstance(ast, ExprNode) {
            raise SqlError('Expected a scalar SQL expression');
        }
        DataType(ast.dtype.name, ast.dtype.nullable);
        if isinstance(ast, ColumnNode) {
            if not `any([s is ast.source for s in scope]) {
                raise SqlError(f'Column source is outside scope: {ast.name}');
            }
            actual = ast.source.schema.find(ast.name);
            if not same_type(actual.dtype, ast.dtype) {
                raise SqlError('Column type differs from source schema');
            }
            return Checked(free={_key(ast.source, ast.name)});
        }
        if isinstance(ast, ParamNode) {
            validate_value(ast.dtype, ast.value);
            return Checked(free=set());
        }
        if isinstance(ast, BinaryNode) {
            a = self.expr(ast.left, scope, local, ctes);
            b = self.expr(ast.right, scope, local, ctes);
            if not same_type(ast.left.dtype, ast.right.dtype) {
                raise SqlError('Binary operands have different SQL types');
            }
            expected: DataType;
            if ast.op in ('=', '>') {
                if ast.op == '>'
                    and ast.left.dtype.name
                        not in ('bigint', 'double precision', 'text') {
                    raise SqlError('Unsupported ordered comparison');
                }
                expected = DataType('boolean', ast.left.dtype.nullable);
            } elif ast.op == '+' {
                if ast.left.dtype.name != 'bigint' or ast.left.dtype.nullable {
                    raise SqlError('Addition expects non-null int64');
                }
                expected = DataType('bigint');
            } else {
                raise SqlError('Unsupported binary operator');
            }
            if not same_type(expected, ast.dtype) {
                raise SqlError('Invalid binary result type');
            }
            return Checked(free=a.free | b.free, aggregate=a.aggregate or b.aggregate);
        }
        if isinstance(ast, BoolNode) {
            if ast.op != 'AND'
                or not ast.terms
                or not same_type(ast.dtype, DataType('boolean')) {
                raise SqlError('Invalid boolean ast');
            }
            checked = [self.expr(t, scope, local, ctes) for t in ast.terms];
            free: set[str] = set();
            for (term, result) in zip(ast.terms, checked) {
                if not same_type(term.dtype, DataType('boolean')) {
                    raise SqlError('AND expects non-null booleans');
                }
                free |= result.free;
            }
            return Checked(free=free, aggregate=`any([c.aggregate for c in checked]));
        }
        if isinstance(ast, UnaryNode) {
            term = self.expr(ast.term, scope, local, ctes);
            if ast.op != 'IS NULL'
                or not ast.term.dtype.nullable
                or not same_type(ast.dtype, DataType('boolean')) {
                raise SqlError('Invalid IS NULL ast');
            }
            return Checked(free=term.free, aggregate=term.aggregate);
        }
        if isinstance(ast, CastNode) {
            term = self.expr(ast.term, scope, local, ctes);
            if ast.term.dtype.nullable and not ast.dtype.nullable {
                raise SqlError('CAST cannot remove nullability');
            }
            return Checked(free=term.free, aggregate=term.aggregate);
        }
        if isinstance(ast, AggregateNode) {
            if ast.op == 'COUNT'
                and ast.term is None
                and same_type(ast.dtype, DataType('bigint')) {
                return Checked(free=set(), aggregate=True);
            }
            if ast.op == 'SUM' and ast.term is not None {
                term = self.expr(ast.term, scope, local, ctes);
                if term.aggregate {
                    raise SqlError('Nested aggregates require a subquery');
                }
                local_keys = {_key(s, f.name) for s in local for f in s.schema.fields};
                if not term.free <= local_keys {
                    raise SqlError(
                        'Outer-column aggregation requires an explicit query region'
                    );
                }
                if not same_type(ast.term.dtype, DataType('double precision'))
                    or not same_type(ast.dtype, DataType('double precision', True)) {
                    raise SqlError('Invalid SUM type');
                }
                return Checked(free=set(), aggregate=True);
            }
            raise SqlError('Unsupported aggregate');
        }
        if isinstance(ast, CoalesceNode) {
            a = self.expr(ast.term, scope, local, ctes);
            b = self.expr(ast.fallback, scope, local, ctes);
            if not ast.term.dtype.nullable
                or ast.fallback.dtype.nullable
                or ast.term.dtype.name != ast.fallback.dtype.name
                or not same_type(ast.dtype, ast.fallback.dtype) {
                raise SqlError('Invalid COALESCE type');
            }
            return Checked(free=a.free | b.free, aggregate=a.aggregate or b.aggregate);
        }
        if isinstance(ast, ScalarNode) {
            q = self.query(ast.query, scope, ctes);
            fields = ast.query.schema.fields;
            allowed = ('exactly_one_aggregate', )
                if ast.require_one
                else ('exactly_one_aggregate', 'at_most_one');
            if len(fields) != 1 or ast.query.cardinality not in allowed {
                raise SqlError('Scalar query cardinality/schema violation');
            }
            expected = fields[0].dtype
                if ast.require_one
                else DataType(fields[0].dtype.name, True);
            if not same_type(expected, ast.dtype) {
                raise SqlError('Scalar query result type mismatch');
            }
            return Checked(free=q.external);
        }
        if isinstance(ast, ExistsNode) {
            q = self.query(ast.query, scope, ctes);
            if not same_type(ast.dtype, DataType('boolean')) {
                raise SqlError('EXISTS returns a non-null boolean');
            }
            return Checked(free=q.external);
        }
        raise SqlError('Unknown scalar SQL ast');
    }

    def query(ast: RelationNode, outer: list[Source], ctes: list[Cte]) -> QueryFacts {
        if not isinstance(ast, RelationNode) {
            raise SqlError('Expected a relation ast');
        }
        if id(ast) in self.active_queries {
            raise SqlError('Cyclic AST: use a recursive CTE reference');
        }
        self.active_queries.add(id(ast));
        try {
            return self.query_body(ast, outer, ctes);
        } finally {
            self.active_queries.remove(id(ast));
        }
    }

    def query_body(
        ast: RelationNode, outer: list[Source], ctes: list[Cte]
    ) -> QueryFacts {
        Schema(tuple(ast.schema.fields));
        if isinstance(ast, SelectNode) {
            return self.select_sql(ast, outer, ctes);
        }
        if isinstance(ast, UnionNode) {
            validate_union(ast);
            a = self.query(ast.left, outer, ctes);
            b = self.query(ast.right, outer, ctes);
            return QueryFacts(external=a.external | b.external);
        }
        raise SqlError('Unknown relational ast');
    }

    def select_sql(
        ast: SelectNode, outer: list[Source], ctes: list[Cte]
    ) -> QueryFacts {
        fields = [p.field for p in ast.projections];
        Schema(tuple(fields));
        for projection in ast.projections {
            if not same_type(projection.field.dtype, projection.expr.dtype) {
                raise SqlError(
                    f'SELECT projection {projection.field.name}: expression type differs from field'
                );
            }
        }
        if ast.limit is not None and (type(ast.limit) is not int or ast.limit < 0) {
            raise SqlError('Invalid LIMIT');
        }
        if ast.cardinality == 'at_most_one' and ast.limit != 1 {
            raise SqlError('At-most-one proof requires LIMIT 1');
        }
        if ast.cardinality not in ('many', 'at_most_one', 'exactly_one_aggregate') {
            raise SqlError('Unknown cardinality proof');
        }
        local: list[Source] = [];
        used_aliases: set[str] = set();
        all_free: set[str] = set();
        if ast.source is not None {
            local.append(ast.source);
            used_aliases.add(self.alias_for(ast.source));
            self.source(ast.source, ctes);
        } elif ast.joins {
            raise SqlError('JOIN requires a FROM source');
        }
        for join in ast.joins {
            if self.alias_for(join.source) in used_aliases
                or `any([s is join.source for s in local]) {
                raise SqlError('Duplicate source binding/alias');
            }
            local.append(join.source);
            used_aliases.add(self.alias_for(join.source));
            condition = self.expr(join.condition, local + outer, local, ctes);
            if join.condition.dtype.name != 'boolean' or condition.aggregate {
                raise SqlError('JOIN ON requires a non-aggregate predicate');
            }
            all_free |= condition.free;
            self.source(join.source, ctes);
        }
        if `any([self.alias_for(s) in used_aliases for s in outer]) {
            raise SqlError('Nested alias shadows a correlated source');
        }
        scope = local + outer;
        projected = [self.expr(p.expr, scope, local, ctes) for p in ast.projections];
        groups = [self.expr(g, scope, local, ctes) for g in ast.groups];
        if `any([g.aggregate for g in groups]) {
            raise SqlError('GROUP BY cannot contain an aggregate');
        }
        # Initial fragment groups by columns, keeping functional-dependency proof explicit.
        if `any([not isinstance(g, ColumnNode) for g in ast.groups]) {
            raise SqlError('GROUP BY currently accepts column expressions');
        }
        grouped: set[str] = set();
        for g in groups {
            grouped |= g.free;
        }
        if ast.predicate is not None {
            pred = self.expr(ast.predicate, scope, local, ctes);
            if ast.predicate.dtype.name != 'boolean' or pred.aggregate {
                raise SqlError('WHERE requires a non-aggregate boolean');
            }
            all_free |= pred.free;
        }
        having: Checked | None = None;
        if ast.having is not None {
            having = self.expr(ast.having, scope, local, ctes);
            if ast.having.dtype.name != 'boolean' {
                raise SqlError('HAVING requires a boolean');
            }
        }
        ordered = [self.expr(o.expr, scope, local, ctes) for o in ast.ordering];
        checked = projected + ordered + ([having] if having is not None else []);
        is_aggregate = bool(groups)
            or having is not None
            or `any([v.aggregate for v in checked]);
        if ast.cardinality == 'exactly_one_aggregate'
            and (
                groups
                or ast.having is not None
                or ast.limit is not None
                or not `any([v.aggregate for v in projected])
            ) {
            raise SqlError(
                'Exactly-one aggregate proof requires an ungrouped, unfiltered aggregate result'
            );
        }
        local_keys = {_key(s, f.name) for s in local for f in s.schema.fields};
        for v in checked {
            all_free |= v.free;
            if is_aggregate and not (v.free & local_keys) <= grouped {
                raise SqlError('Non-aggregate column is missing from GROUP BY');
            }
        }
        for g in groups {
            all_free |= g.free;
        }
        return QueryFacts(external=all_free - local_keys);
    }
}


"""Render an already validated query; semantic rules live in QueryValidator."""
obj PostgresRenderer {
    has params: dict[str, bool | int | float | str | UUID | None] = {},
        parameter_ids: dict[int, str] = {},
        aliases: dict[int, str] = {},
        cte_names: dict[int, str] = {};

    def alias_for(src: Source) -> str {
        return quote_identifier(self.aliases[id(src)]);
    }

    def render(plan: ValidatedQuery) -> CompiledSQL {
        self.params = {};
        self.parameter_ids = {};
        self.aliases = plan.aliases;
        self.cte_names = plan.cte_names;
        definitions: list[str] = [];
        for reference in plan.ctes {
            definition = reference.definition;
            if isinstance(definition, UnionNode) and reference.recursive {
                body = 'SELECT * FROM ('
                    + self.query(definition.left)
                    + ') AS "_recursive_anchor" UNION ALL '
                    + self.query(definition.right);
            } elif definition is not None {
                body = self.query(definition);
            } else {
                raise SqlError('Unvalidated CTE definition');
            }
            columns = ', '.join(
                [quote_identifier(f.name) for f in reference.schema.fields]
            );
            definitions.append(
                quote_identifier(self.cte_names[id(reference)])
                    + ' ('
                    + columns
                    + ') AS ('
                    + body
                    + ')'
            );
        }
        prefix = '';
        if definitions {
            prefix = 'WITH '
                + ('RECURSIVE ' if `any([c.recursive for c in plan.ctes]) else '')
                + ', '.join(definitions)
                + ' ';
        }
        return CompiledSQL(
            sql=prefix + self.query(plan.query), params=dict(self.params)
        );
    }

    def source(src: Source) -> str {
        if isinstance(src, Table) {
            name = '.'.join([quote_identifier(p) for p in src.name]);
        } elif isinstance(src, Derived) {
            name = '(' + self.query(src.query) + ')';
        } elif isinstance(src, (Cte, CteUse)) {
            reference = src.target if isinstance(src, CteUse) else src;
            name = quote_identifier(self.cte_names[id(reference)]);
        } else {
            raise SqlError('Unvalidated source');
        }
        return name + ' AS ' + self.alias_for(src);
    }

    def expr(ast: ExprNode) -> str {
        if isinstance(ast, ColumnNode) {
            return self.alias_for(ast.source) + '.' + quote_identifier(ast.name);
        }
        if isinstance(ast, ParamNode) {
            identity = id(ast);
            if identity not in self.parameter_ids {
                key = 'p' + str(len(self.params));
                self.parameter_ids[identity] = key;
                self.params[key] = ast.value;
            }
            return 'CAST(:'
                + self.parameter_ids[identity]
                + ' AS '
                + ast.dtype.name
                + ')';
        }
        if isinstance(ast, BinaryNode) {
            return '('
                + self.expr(ast.left)
                + ' '
                + ast.op
                + ' '
                + self.expr(ast.right)
                + ')';
        }
        if isinstance(ast, BoolNode) {
            return '(' + ' AND '.join([self.expr(t) for t in ast.terms]) + ')';
        }
        if isinstance(ast, UnaryNode) {
            return '(' + self.expr(ast.term) + ' IS NULL)';
        }
        if isinstance(ast, CastNode) {
            return 'CAST(' + self.expr(ast.term) + ' AS ' + ast.dtype.name + ')';
        }
        if isinstance(ast, AggregateNode) {
            return 'COUNT(*)'
                if ast.term is None
                else 'SUM(' + self.expr(ast.term) + ')';
        }
        if isinstance(ast, CoalesceNode) {
            return 'COALESCE('
                + self.expr(ast.term)
                + ', '
                + self.expr(ast.fallback)
                + ')';
        }
        if isinstance(ast, ScalarNode) {
            return '(' + self.query(ast.query) + ')';
        }
        if isinstance(ast, ExistsNode) {
            return 'EXISTS (' + self.query(ast.query) + ')';
        }
        raise SqlError('Unvalidated expression');
    }

    def query(ast: RelationNode) -> str {
        if isinstance(ast, UnionNode) {
            op = ' UNION ALL ' if ast.keep_duplicates else ' UNION ';
            return 'SELECT * FROM ('
                + self.query(ast.left)
                + ') AS "_union_l"'
                + op
                + 'SELECT * FROM ('
                + self.query(ast.right)
                + ') AS "_union_r"';
        }
        if not isinstance(ast, SelectNode) {
            raise SqlError('Unvalidated relation');
        }
        from_sql = '';
        if ast.source is not None {
            from_sql = ' FROM ' + self.source(ast.source);
        }
        for join in ast.joins {
            condition = self.expr(join.condition);
            from_sql += ' INNER JOIN ' + self.source(join.source) + ' ON ' + condition;
        }
        projected = [
            self.expr(p.expr) + ' AS ' + quote_identifier(p.field.name)
            for p in ast.projections
        ];
        groups = [self.expr(g) for g in ast.groups];
        predicate = ' WHERE ' + self.expr(ast.predicate)
            if ast.predicate is not None
            else '';
        having = ' HAVING ' + self.expr(ast.having) if ast.having is not None else '';
        ordered = [
            self.expr(o.expr) + (' DESC' if o.descending else ' ASC')
            for o in ast.ordering
        ];
        return 'SELECT '
            + ', '.join(projected)
            + from_sql
            + predicate
            + (' GROUP BY ' + ', '.join(groups) if groups else '')
            + having
            + (' ORDER BY ' + ', '.join(ordered) if ordered else '')
            + (' LIMIT ' + str(ast.limit) if ast.limit is not None else '');
    }
}


def compile_sql[R, C](query: Relation[R, C]) -> CompiledSQL {
    plan = QueryValidator().analyze(query);
    return PostgresRenderer().render(plan);
}


def validate_recursive_step(ref: Cte, step: SelectNode) -> None {
    sources = ([step.source] if step.source is not None else [])
        + [j.source for j in step.joins];
    if len(
        [
            s
            for s in sources
            if s is ref or (isinstance(s, CteUse) and s.target is ref)
        ]
    )
        != 1 {
        raise SqlError('Recursive step requires exactly one direct self-reference');
    }
    if `any([isinstance(s, Derived) for s in sources])
        or step.groups
        or step.having is not None
        or step.ordering
        or step.limit is not None {
        raise SqlError(
            'Recursive step supports direct sources and ungrouped, unordered rows'
        );
    }
    work = [p.expr for p in step.projections] + [j.condition for j in step.joins];
    if step.predicate is not None {
        work.append(step.predicate);
    }
    while work {
        expr = work.pop();
        if isinstance(expr, (ColumnNode, ParamNode)) {
            continue;
        }
        if isinstance(expr, BinaryNode) {
            work.extend([expr.left, expr.right]);
        } elif isinstance(expr, BoolNode) {
            work.extend(expr.terms);
        } elif isinstance(expr, (UnaryNode, CastNode)) {
            work.append(expr.term);
        } elif isinstance(expr, CoalesceNode) {
            work.extend([expr.term, expr.fallback]);
        } else {
            raise SqlError(
                'Recursive step scalar fragment excludes aggregates and subqueries'
            );
        }
    }
}
