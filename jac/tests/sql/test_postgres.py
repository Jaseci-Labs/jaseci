"""Run the same behavioral cases on an explicitly supplied disposable PostgreSQL.

JAC_SQL_PG_SOCKET=/path/to/.s.PGSQL.PORT python -m unittest discover -s jac/tests/sql -p test_postgres.py
"""
import os
import unittest
from jaclang import sql as s
import test_sql


class Rows:
    def __init__(self, values):
        self.values = values

    def fetchall(self):
        return self.values

    def fetchone(self):
        return self.values[0] if self.values else None


class Database:
    def __init__(self):
        from jaclang.data.pgwire import PgWireConnection
        self.connection = PgWireConnection(user='sql_test', unix_sock=os.environ['JAC_SQL_PG_SOCKET'], database='postgres')
        self.connection.run('BEGIN')

    def execute(self, sql, params=None):
        return Rows(self.connection.run(sql, **(params or {})))

    def executescript(self, script):
        # These scripts are fixed test fixture literals, not user queries.
        for statement in script.split(';'):
            if statement.strip():
                self.connection.run(statement)

    def close(self):
        try:
            self.connection.run('ROLLBACK')
        finally:
            self.connection.close()


@unittest.skipUnless(os.environ.get('JAC_SQL_PG_SOCKET'), 'Set socket of a disposable SQL test cluster')
class PostgresTests(test_sql.SQLTests):
    def setUp(self):
        self.id = s.field('id', s.int64_type())
        self.age = s.field('age', s.int64_type())
        self.name = s.field('name', s.text_type())
        self.people = s.table('people', [self.id, self.age, self.name], 'p')
        self.db = Database()
        self.addCleanup(self.db.close)
        self.db.executescript('CREATE TEMP TABLE people(id BIGINT, age BIGINT, name TEXT);'
                              "INSERT INTO people VALUES(1,20,'Ann'),(2,40,'Bob'),(3,40,'Cora');")
