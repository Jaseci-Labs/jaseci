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

obj DataType {
    has name: str,
        nullable: bool = False;

    def postinit {
        if self.name not in ('boolean', 'bigint', 'double precision', 'text', 'uuid') {
            raise SqlError(f"Unsupported SQL type: {self.name}");
        }
    }
}

obj SqlType[T] {
    has data: DataType;
}

obj FieldDef {
    has name: str,
        dtype: DataType;
}

obj Field[T](FieldDef) {}

obj Schema {
    has fields: list[FieldDef];

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

obj RelationNode {
    has schema: Schema,
        cardinality: str;
}

obj Source {
    has schema: Schema,
        alias: str;

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
    has name: list[str];
}

obj Derived(Source) {
    has query: RelationNode;
}

obj Cte(Source) {
    has name: str;
}

obj ExprNode {
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
        terms: list[ExprNode];
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

obj ScalarExpr[T] {
    has ast: ExprNode;
}

obj ProjectionDef {
    has field: FieldDef,
        expr: ExprNode;
}

obj Projection[T](ProjectionDef) {
    def key -> Field[T] {
        return Field(name=self.field.name, dtype=self.field.dtype);
    }
}

obj Order {
    has expr: ExprNode,
        descending: bool;
}

obj Join {
    has source: Source,
        condition: ExprNode;
}

obj SelectNode(RelationNode) {
    has projections: list[ProjectionDef],
        source: Source | None,
        joins: list[Join],
        predicate: ExprNode | None,
        groups: list[ExprNode],
        having: ExprNode | None,
        ordering: list[Order],
        limit: int | None;
}

obj UnionNode(RelationNode) {
    has left: RelationNode,
        right: RelationNode,
        keep_duplicates: bool;
}

obj CteBinding {
    has reference: Cte,
        query: RelationNode;
}

obj WithNode(RelationNode) {
    has bindings: list[CteBinding],
        body: RelationNode,
        recursive: bool;
}

obj Relation[R, C] {
    has ast: RelationNode;

    def as_source(alias: str) -> Source {
        return Derived(schema=self.ast.schema, alias=alias, query=self.ast);
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
    name: str, fields: list[FieldDef], alias: str, namespace: str | None = None
) -> Source {
    parts = [name] if namespace is None else [namespace, name];
    return Table(schema=Schema(fields), alias=alias, name=parts);
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
        BoolNode(dtype=DataType('boolean'), op='AND', terms=[t.ast for t in terms])
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

def select_(
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
    schema = Schema([p.field for p in projections]);
    return Relation(
        SelectNode(
            schema=schema,
            cardinality='many',
            projections=list(projections),
            source=source,
            joins=list(joins),
            predicate=where.ast if where is not None else None,
            groups=list(group_by),
            having=having.ast if having is not None else None,
            ordering=list(order_by),
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
        schema=q.schema,
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
    q = select_(projections, source=source, where=where);
    q.ast.cardinality = 'exactly_one_aggregate';
    return Relation(q.ast);
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
            schema=left.ast.schema,
            cardinality='many',
            left=left.ast,
            right=right.ast,
            keep_duplicates=True
        )
    );
}

def cte(name: str, fields: list[FieldDef], alias: str) -> Cte {
    return Cte(schema=Schema(fields), alias=alias, name=name);
}

def bind_cte[R, C](reference: Cte, query: Relation[R, C]) -> CteBinding {
    a = reference.schema.fields;
    b = query.ast.schema.fields;
    if len(a) != len(b)
        or not all([same_type(x.dtype, y.dtype) for (x, y) in zip(a, b)]) {
        raise SqlError('CTE output schema differs from declared schema');
    }
    return CteBinding(reference=reference, query=query.ast);
}

def with_ctes[R, C](
    bindings: list[CteBinding], body: Relation[R, C], recursive: bool = False
) -> Relation[R, C] {
    return Relation(
        WithNode(
            schema=body.ast.schema,
            cardinality=body.ast.cardinality,
            bindings=list(bindings),
            body=body.ast,
            recursive=recursive
        )
    );
}


"""PostgreSQL rendering plus structural validation; SQL strings are emitted here."""
obj Checked {
    has sql: str,
        free: set[str],
        aggregate: bool = False;
}

obj QueryText {
    has sql: str,
        external: set[str];
}


def quote_identifier(name: str) -> str {
    if not isinstance(name, str) or not name or '\x00' in name {
        raise SqlError('Identifier must be a nonempty string without NUL');
    }
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

obj PostgresRenderer {
    has params: dict[str, bool | int | float | str | UUID | None] = {},
        parameter_ids: dict[int, str] = {},
        active_queries: set[int] = set();

    def compile[R, C](query: Relation[R, C]) -> CompiledSQL {
        if not isinstance(query, Relation) {
            raise SqlError('Expected a relation, not a scalar or command');
        }
        self.params = {};
        self.parameter_ids = {};
        self.active_queries = set();
        rendered = self.query(query.ast, [], []);
        if rendered.external {
            raise SqlError('Top-level query has unbound correlations');
        }
        return CompiledSQL(sql=rendered.sql, params=dict(self.params));
    }

    def source(src: Source, ctes: list[Cte]) -> str {
        Schema(list(src.schema.fields));
        alias = quote_identifier(src.alias);
        if isinstance(src, Table) {
            if not src.name {
                raise SqlError('Table needs a name');
            }
            return '.'.join([quote_identifier(p) for p in src.name]) + ' AS ' + alias;
        }
        if isinstance(src, Derived) {
            if not _schema_equal(src.schema, src.query.schema) {
                raise SqlError('Derived schema mismatch');
            }
            q = self.query(src.query, [], ctes);
            if q.external {
                raise SqlError('FROM subquery requires LATERAL for correlations');
            }
            return '(' + q.sql + ') AS ' + alias;
        }
        if isinstance(src, Cte) {
            if not `any([x is src for x in ctes]) {
                raise SqlError(f'CTE is outside scope: {src.name}');
            }
            return quote_identifier(src.name) + ' AS ' + alias;
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
            return Checked(
                sql=quote_identifier(ast.source.alias)
                    + '.'
                    + quote_identifier(ast.name),
                free={_key(ast.source, ast.name)}
            );
        }
        if isinstance(ast, ParamNode) {
            validate_value(ast.dtype, ast.value);
            identity = id(ast);
            if identity not in self.parameter_ids {
                key = 'p' + str(len(self.params));
                self.parameter_ids[identity] = key;
                self.params[key] = ast.value;
            }
            return Checked(
                sql='CAST(:'
                    + self.parameter_ids[identity]
                    + ' AS '
                    + ast.dtype.name
                    + ')',
                free=set()
            );
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
            return Checked(
                sql='(' + a.sql + ' ' + ast.op + ' ' + b.sql + ')',
                free=a.free | b.free,
                aggregate=a.aggregate or b.aggregate
            );
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
            return Checked(
                sql='(' + ' AND '.join([c.sql for c in checked]) + ')',
                free=free,
                aggregate=`any([c.aggregate for c in checked])
            );
        }
        if isinstance(ast, UnaryNode) {
            term = self.expr(ast.term, scope, local, ctes);
            if ast.op != 'IS NULL'
                or not ast.term.dtype.nullable
                or not same_type(ast.dtype, DataType('boolean')) {
                raise SqlError('Invalid IS NULL ast');
            }
            return Checked(
                sql='(' + term.sql + ' IS NULL)',
                free=term.free,
                aggregate=term.aggregate
            );
        }
        if isinstance(ast, CastNode) {
            term = self.expr(ast.term, scope, local, ctes);
            if ast.term.dtype.nullable and not ast.dtype.nullable {
                raise SqlError('CAST cannot remove nullability');
            }
            return Checked(
                sql='CAST(' + term.sql + ' AS ' + ast.dtype.name + ')',
                free=term.free,
                aggregate=term.aggregate
            );
        }
        if isinstance(ast, AggregateNode) {
            if ast.op == 'COUNT'
                and ast.term is None
                and same_type(ast.dtype, DataType('bigint')) {
                return Checked(sql='COUNT(*)', free=set(), aggregate=True);
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
                return Checked(sql='SUM(' + term.sql + ')', free=set(), aggregate=True);
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
            return Checked(
                sql='COALESCE(' + a.sql + ', ' + b.sql + ')',
                free=a.free | b.free,
                aggregate=a.aggregate or b.aggregate
            );
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
            return Checked(sql='(' + q.sql + ')', free=q.external);
        }
        if isinstance(ast, ExistsNode) {
            q = self.query(ast.query, scope, ctes);
            if not same_type(ast.dtype, DataType('boolean')) {
                raise SqlError('EXISTS returns a non-null boolean');
            }
            return Checked(sql='EXISTS (' + q.sql + ')', free=q.external);
        }
        raise SqlError('Unknown scalar SQL ast');
    }

    def query(ast: RelationNode, outer: list[Source], ctes: list[Cte]) -> QueryText {
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
    ) -> QueryText {
        Schema(list(ast.schema.fields));
        if isinstance(ast, SelectNode) {
            return self.select_sql(ast, outer, ctes);
        }
        if isinstance(ast, UnionNode) {
            if not _schema_equal(ast.schema, ast.left.schema)
                or not _schema_equal(ast.left.schema, ast.right.schema, False)
                or ast.cardinality != 'many' {
                raise SqlError('UNION schema/cardinality mismatch');
            }
            a = self.query(ast.left, outer, ctes);
            b = self.query(ast.right, outer, ctes);
            op = ' UNION ALL ' if ast.keep_duplicates else ' UNION ';
            # Derived wrappers make arm-local ORDER/LIMIT unambiguous in PostgreSQL and SQLite.
            return QueryText(
                sql='SELECT * FROM ('
                    + a.sql
                    + ') AS "_union_l"'
                    + op
                    + 'SELECT * FROM ('
                    + b.sql
                    + ') AS "_union_r"',
                external=a.external | b.external
            );
        }
        if isinstance(ast, WithNode) {
            if not _schema_equal(ast.schema, ast.body.schema)
                or ast.cardinality != ast.body.cardinality {
                raise SqlError('WITH output mismatch');
            }
            names = {c.name for c in ctes};
            available = list(ctes);
            parts: list[str] = [];
            for binding in ast.bindings {
                ref = binding.reference;
                if ref.name in names {
                    raise SqlError('Duplicate CTE name');
                }
                if not _schema_equal(ref.schema, binding.query.schema, False) {
                    raise SqlError('CTE schema mismatch');
                }
                names.add(ref.name);
                # Explicit recursive references are accepted only in the recursive UNION ALL arm.
                if ast.recursive {
                    if not isinstance(binding.query, UnionNode)
                        or not binding.query.keep_duplicates {
                        raise SqlError('Recursive binding requires UNION ALL');
                    }
                    body = binding.query;
                    if not isinstance(body.left, SelectNode)
                        or not isinstance(body.right, SelectNode) {
                        raise SqlError(
                            'Recursive CTE requires a SELECT anchor and SELECT step'
                        );
                    }
                    validate_recursive_step(ref, body.right);
                    a = self.query(body.left, [], available);
                    b = self.query(body.right, [], available + [ref]);
                    sql = a.sql + ' UNION ALL ' + b.sql;
                } else {
                    sql = self.query(binding.query, [], available).sql;
                }
                columns = ', '.join(
                    [quote_identifier(f.name) for f in ref.schema.fields]
                );
                parts.append(
                    quote_identifier(ref.name) + ' (' + columns + ') AS (' + sql + ')'
                );
                available.append(ref);
            }
            if not parts {
                raise SqlError('WITH requires at least one binding');
            }
            result = self.query(ast.body, outer, available);
            return QueryText(
                sql='WITH '
                    + ('RECURSIVE ' if ast.recursive else '')
                    + ', '.join(parts)
                    + ' '
                    + result.sql,
                external=result.external
            );
        }
        raise SqlError('Unknown relational ast');
    }

    def select_sql(ast: SelectNode, outer: list[Source], ctes: list[Cte]) -> QueryText {
        fields = [p.field for p in ast.projections];
        if not _schema_equal(ast.schema, Schema(fields)) {
            raise SqlError('SELECT schema differs from projections');
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
        from_sql = '';
        all_free: set[str] = set();
        if ast.source is not None {
            local.append(ast.source);
            used_aliases.add(ast.source.alias);
            from_sql = ' FROM ' + self.source(ast.source, ctes);
        } elif ast.joins {
            raise SqlError('JOIN requires a FROM source');
        }
        for join in ast.joins {
            if join.source.alias in used_aliases
                or `any([s is join.source for s in local]) {
                raise SqlError('Duplicate source binding/alias');
            }
            local.append(join.source);
            used_aliases.add(join.source.alias);
            condition = self.expr(join.condition, local + outer, local, ctes);
            if join.condition.dtype.name != 'boolean' or condition.aggregate {
                raise SqlError('JOIN ON requires a non-aggregate predicate');
            }
            all_free |= condition.free;
            from_sql += ' INNER JOIN '
                + self.source(join.source, ctes)
                + ' ON '
                + condition.sql;
        }
        if `any([s.alias in used_aliases for s in outer]) {
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
        predicate_sql = '';
        having_sql = '';
        ordering_sql = '';
        if ast.predicate is not None {
            pred = self.expr(ast.predicate, scope, local, ctes);
            if ast.predicate.dtype.name != 'boolean' or pred.aggregate {
                raise SqlError('WHERE requires a non-aggregate boolean');
            }
            all_free |= pred.free;
            predicate_sql = ' WHERE ' + pred.sql;
        }
        having: Checked | None = None;
        if ast.having is not None {
            having = self.expr(ast.having, scope, local, ctes);
            if ast.having.dtype.name != 'boolean' {
                raise SqlError('HAVING requires a boolean');
            }
            having_sql = ' HAVING ' + having.sql;
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
        for v in checked {
            all_free |= v.free;
            if is_aggregate and not v.free <= grouped {
                raise SqlError('Non-aggregate column is missing from GROUP BY');
            }
        }
        for g in groups {
            all_free |= g.free;
        }
        projection_sql = ', '.join(
            [
                v.sql + ' AS ' + quote_identifier(p.field.name)
                for (p, v) in zip(ast.projections, projected)
            ]
        );
        group_sql = ' GROUP BY ' + ', '.join([g.sql for g in groups]) if groups else '';
        if ordered {
            ordering_sql = ' ORDER BY '
                + ', '.join(
                    [
                        v.sql + (' DESC' if o.descending else ' ASC')
                        for (o, v) in zip(ast.ordering, ordered)
                    ]
                );
        }
        limit_sql = ' LIMIT ' + str(ast.limit) if ast.limit is not None else '';
        local_keys = {_key(s, f.name) for s in local for f in s.schema.fields};
        return QueryText(
            sql='SELECT '
                + projection_sql
                + from_sql
                + predicate_sql
                + group_sql
                + having_sql
                + ordering_sql
                + limit_sql,
            external=all_free - local_keys
        );
    }
}


def compile_sql[R, C](query: Relation[R, C]) -> CompiledSQL {
    return PostgresRenderer().compile(query);
}


def validate_recursive_step(ref: Cte, step: SelectNode) -> None {
    sources = ([step.source] if step.source is not None else [])
        + [j.source for j in step.joins];
    if len(
        [
            s
            for s in sources
            if s is ref
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
