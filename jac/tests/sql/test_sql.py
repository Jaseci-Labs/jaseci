"""Behavioral contracts for the portable Jac SQL package (stdlib unittest/sqlite3)."""
import sqlite3
import importlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from uuid import UUID

from jaclang import sql as s


class SQLTests(unittest.TestCase):
    def setUp(self):
        self.id = s.field('id', s.int64_type())
        self.age = s.field('age', s.int64_type())
        self.name = s.field('name', s.text_type())
        self.people = s.table('people', [self.id, self.age, self.name], 'p')
        self.db = sqlite3.connect(':memory:')
        self.db.executescript('CREATE TABLE people(id INTEGER, age INTEGER, name TEXT);'
                              "INSERT INTO people VALUES(1,20,'Ann'),(2,40,'Bob'),(3,40,'Cora');")
        self.addCleanup(self.db.close)

    def execute(self, query):
        c = s.compile_sql(query)
        return self.db.execute(c.sql, c.params).fetchall()

    def test_module_is_portable_as_one_file(self):
        with TemporaryDirectory(prefix='jac-sql-portable-') as folder:
            module=Path(folder)/'portable_sql.jac'
            module.write_text(Path(s.__file__).read_text())
            sys.path.insert(0,folder)
            try:
                independent=importlib.import_module('portable_sql')
                query=independent.select_([independent.named('n',independent.int64(7))])
                compiled=independent.compile_sql(query)
                self.assertEqual(self.db.execute(compiled.sql,compiled.params).fetchone(),(7,))
            finally:
                sys.path.remove(folder)
                sys.modules.pop('portable_sql',None)

    def test_select_parameters_and_order(self):
        q = s.select_([s.named('name', self.people.col(self.name))], source=self.people,
                      where=s.gt(self.people.col(self.age), s.int64(30)),
                      order_by=[s.desc(self.people.col(self.name))])
        self.assertEqual(self.execute(q), [('Cora',), ('Bob',)])
        c = s.compile_sql(q)
        self.assertEqual(c.params, {'p0': 30})
        self.assertIn(':p0', c.sql)

    def test_join_and_shared_parameter(self):
        age = self.people.col(self.age)
        p = s.int64(30)
        q = s.select_([s.named('plus', s.add(age, p))], source=self.people,
                      where=s.gt(age, p))
        self.assertEqual(self.execute(q), [(70,), (70,)])
        self.assertEqual(s.compile_sql(q).params, {'p0': 30})
        owner = s.field('owner', s.int64_type())
        pets = s.table('pets', [owner], 'pet')
        self.db.executescript('CREATE TABLE pets(owner INTEGER); INSERT INTO pets VALUES(2),(2);')
        join = s.inner_join(pets, s.eq(self.people.col(self.id), pets.col(owner)))
        q = s.select_([s.named('name', self.people.col(self.name))], source=self.people, joins=[join])
        self.assertEqual(self.execute(q), [('Bob',), ('Bob',)])

    def test_group_by_count(self):
        key = self.people.col(self.age)
        q = s.select_([s.named('age', key), s.named('n', s.count())], source=self.people,
                      group_by=[key.ast], order_by=[s.asc(key)])
        self.assertEqual(self.execute(q), [(20, 1), (40, 2)])

    def test_aggregate_empty_is_one_row(self):
        result = s.named('n', s.count())
        q = s.aggregate([result], source=self.people,
                        where=s.gt(self.people.col(self.age), s.int64(100)))
        value = s.scalar_one(q, result.key())
        self.assertEqual(self.execute(s.select_([s.named('n', value)])), [(0,)])

    def test_scalar_optional_empty_yields_null(self):
        result = s.named('age', self.people.col(self.age))
        q = s.limit_one(s.select_([result], source=self.people,
                                 where=s.gt(self.people.col(self.age), s.int64(100))))
        value = s.scalar(q, result.key())
        self.assertEqual(self.execute(s.select_([s.named('age', value)])), [(None,)])

    def test_scalar_requires_proof_and_one_column(self):
        result = s.named('age', self.people.col(self.age))
        q = s.select_([result], source=self.people)
        with self.assertRaisesRegex(s.SqlError, 'at-most-one'):
            s.scalar(q, result.key())
        q = s.limit_one(s.select_([result, s.named('name', self.people.col(self.name))], source=self.people))
        with self.assertRaises(s.SqlError):
            s.scalar(q, result.key())

    def test_correlated_exists(self):
        other = s.table('people', [self.id, self.age, self.name], 'other')
        sub = s.select_([s.named('id', other.col(self.id))], source=other,
                        where=s.and_([s.eq(other.col(self.id), self.people.col(self.id)),
                                      s.gt(other.col(self.age), s.int64(30))]))
        q = s.select_([s.named('name', self.people.col(self.name))], source=self.people, where=s.exists(sub))
        self.assertEqual(self.execute(q), [('Bob',), ('Cora',)])

    def test_derived_schema_and_scope(self):
        out = s.named('label', self.people.col(self.name))
        source = s.select_([out], source=self.people).as_source('labels')
        self.assertEqual(self.execute(s.select_([s.named('label', source.col(out.key()))], source=source)), [('Ann',), ('Bob',), ('Cora',)])
        with self.assertRaisesRegex(s.SqlError, 'Unknown column'):
            source.col(self.age)
        with self.assertRaisesRegex(s.SqlError, 'outside scope'):
            s.compile_sql(s.select_([s.named('name', self.people.col(self.name))]))

    def test_union_schema_and_arm_limits(self):
        first = s.select_([s.named('n', s.int64(1))], limit=1)
        second = s.select_([s.named('m', s.int64(2))], limit=1)
        self.assertEqual(self.execute(s.union_all(first, second)), [(1,), (2,)])
        with self.assertRaisesRegex(s.SqlError, 'UNION'):
            s.union_all(first, s.select_([s.named('n', s.text('bad'))]))

    def test_cte(self):
        key = s.field('n', s.int64_type())
        ref = s.cte('numbers', [key], 'n')
        binding = s.bind_cte(ref, s.select_([s.named('n', s.int64(7))]))
        body = s.select_([s.named('n', ref.col(key))], source=ref)
        q = s.with_ctes([binding], body)
        self.assertEqual(self.execute(q), [(7,)])
        with self.assertRaisesRegex(s.SqlError, 'outside scope'):
            s.compile_sql(body)

    def test_recursive_cte(self):
        key = s.field('n', s.int64_type())
        ref = s.cte('walk', [key], 'w')
        first = s.select_([s.named('n', s.int64(1))])
        step = s.select_([s.named('n', s.add(ref.col(key), s.int64(1)))], source=ref,
                         where=s.gt(s.int64(4), ref.col(key)))
        body = s.select_([s.named('n', ref.col(key))], source=ref, order_by=[s.asc(ref.col(key))])
        q = s.with_ctes([s.bind_cte(ref, s.union_all(first, step))], body, recursive=True)
        self.assertEqual(self.execute(q), [(1,), (2,), (3,), (4,)])

    def test_cte_forward_reference_and_recursive_anchor_rejected(self):
        key = s.field('n', s.int64_type())
        a = s.cte('a', [key], 'a')
        b = s.cte('b', [key], 'b')
        from_b = s.select_([s.named('n', b.col(key))], source=b)
        body = s.select_([s.named('n', a.col(key))], source=a)
        q = s.with_ctes([s.bind_cte(a, from_b), s.bind_cte(b, s.select_([s.named('n', s.int64(1))]))], body)
        with self.assertRaises(s.SqlError):
            s.compile_sql(q)
        recursive = s.with_ctes([s.bind_cte(a, s.union_all(body, body))], body, recursive=True)
        with self.assertRaises(s.SqlError):
            s.compile_sql(recursive)

    def test_recursive_step_eligibility(self):
        key=s.field('n',s.int64_type())
        ref=s.cte('walk',[key],'w')
        anchor=s.select_([s.named('n',s.int64(1))])
        steps=[s.select_([s.named('n',s.int64(2))]),
               s.select_([s.named('n',s.count())],source=ref),
               s.select_([s.named('n',ref.col(key))],source=ref,limit=1)]
        body=s.select_([s.named('n',ref.col(key))],source=ref)
        for step in steps:
            query=s.with_ctes([s.bind_cte(ref,s.union_all(anchor,step))],body,recursive=True)
            with self.subTest(step=step), self.assertRaises(s.SqlError):
                s.compile_sql(query)

    def test_nullable_three_valued_predicate(self):
        value = s.param(s.nullable(s.int64_type()), None)
        comparison = s.eq_nullable(value, s.param(s.nullable(s.int64_type()), 3))
        self.assertEqual(self.execute(s.select_([s.named('n', s.int64(1))], where=comparison)), [])
        self.assertEqual(self.execute(s.select_([s.named('n', s.coalesce(value, s.int64(5)))])), [(5,)])
        self.assertEqual(self.execute(s.select_([s.named('missing', s.is_null(value))])), [(1,)])
        with self.assertRaises(s.SqlError):
            s.eq(value, value)

    def test_parameter_value_type_and_bounds(self):
        for dtype, value in [(s.int64_type(), True), (s.int64_type(), '1'),
                             (s.bool_type(), 1), (s.text_type(), 4),
                             (s.int64_type(), 2**63), (s.int64_type(), -2**63-1),
                             (s.uuid_type(), 'bad'), (s.int64_type(), None)]:
            with self.subTest(value=value), self.assertRaises(s.SqlError):
                s.param(dtype, value)
        c=s.compile_sql(s.select_([s.named('id', s.uuid(UUID(int=1)))]))
        self.assertEqual(c.params['p0'], UUID(int=1))
        s.int64(-2**63)
        s.int64(2**63-1)

    def test_injection_is_bound_and_identifiers_are_quoted(self):
        evil = "x'); DROP TABLE people; --"
        c=s.compile_sql(s.select_([s.named('weird"name', s.text(evil))]))
        self.assertNotIn(evil, c.sql)
        self.assertEqual(c.params, {'p0':evil})
        self.assertIn('"weird""name"', c.sql)
        self.assertEqual(self.db.execute(c.sql,c.params).fetchone(), (evil,))
        with self.assertRaises(s.SqlError):
            s.quote_identifier('bad\x00name')

    def test_wrong_expression_categories_and_types(self):
        with self.assertRaises(s.SqlError):
            s.eq(s.int64(1), s.text('a'))
        with self.assertRaises(s.SqlError):
            s.add(s.text('a'), s.text('b'))
        with self.assertRaises(s.SqlError):
            s.and_([s.int64(1)])
        with self.assertRaises(s.SqlError):
            s.select_([s.named('n', s.int64(1))], where=s.int64(1))
        with self.assertRaises(s.SqlError):
            s.compile_sql(s.int64(1))
        with self.assertRaises(s.SqlError):
            s.named('n', s.select_([s.named('n', s.int64(1))]))

    def test_alias_and_join_scopes(self):
        other=s.table('people',[self.id,self.age,self.name],'p')
        join=s.inner_join(other,s.eq(self.people.col(self.id),other.col(self.id)))
        q=s.select_([s.named('n',self.people.col(self.id))],source=self.people,joins=[join])
        with self.assertRaisesRegex(s.SqlError,'Duplicate'):
            s.compile_sql(q)
        future=s.table('people',[self.id],'future')
        other=s.table('people',[self.id],'o')
        bad=s.inner_join(other,s.eq(other.col(self.id),future.col(self.id)))
        q=s.select_([s.named('n',self.people.col(self.id))],source=self.people,joins=[bad])
        with self.assertRaisesRegex(s.SqlError,'outside scope'):
            s.compile_sql(q)

    def test_aggregate_validation(self):
        for q in [s.select_([s.named('age',self.people.col(self.age)),s.named('n',s.count())],source=self.people),
                  s.select_([s.named('age',self.people.col(self.age))],source=self.people,where=s.gt(s.count(),s.int64(1))),
                  s.aggregate([s.named('age',self.people.col(self.age))],source=self.people)]:
            with self.subTest(q=q), self.assertRaises(s.SqlError):
                s.compile_sql(q)

    def test_mutated_ast_is_revalidated(self):
        q=s.limit_one(s.select_([s.named('n',s.int64(1))]))
        value=s.scalar(q,s.field('n',s.int64_type()))
        q.ast.limit=None
        with self.assertRaises(s.SqlError):
            s.compile_sql(s.select_([s.named('n',value)]))
        q=s.select_([s.named('n',s.int64(1))])
        q.ast.projections[0].expr.dtype=s.DataType('text')
        with self.assertRaises(s.SqlError):
            s.compile_sql(q)

    def test_source_field_schema_validation(self):
        with self.assertRaises(s.SqlError):
            self.people.col(s.field('age',s.text_type()))
        with self.assertRaises(s.SqlError):
            s.table('bad',[self.id,self.id],'b')
        for limit in [True,-1,'3']:
            with self.assertRaises(s.SqlError):
                s.select_([s.named('n',s.int64(1))],limit=limit)


if __name__ == '__main__':
    unittest.main()
