import io
import sys
from unittest import TestCase

import jaseci.jac.tests.book_code as jtc
from jaseci.prim.sentinel import Sentinel
from jaseci.prim.graph import Graph
from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import TestCaseHelper


class JacBookTests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()
        self.sent = Sentinel(m_id=0, h=JsOrc.hook())
        self.gph = Graph(m_id=0, h=self.sent._h)
        self.old_stdout = sys.stdout
        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

    def tearDown(self):
        sys.stdout = self.old_stdout
        super().tearDown()

    def to_screen(self):
        sys.stdout = self.old_stdout
        print("output: ", self.new_stdout.getvalue())
        sys.stdout = self.new_stdout

    def screen_on(self):
        sys.stdout = self.old_stdout

    def screen_off(self):
        sys.stdout = self.new_stdout

    def test_spawn_graph_node(self):
        """Test node in using spawn graphs instead of dot"""
        self.sent.register_code(jtc.spawn_graph_node)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "graph_root_node_name\n")

    def test_basic_arith(self):
        self.sent.register_code(jtc.basic_arith)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "8 -20 1.0 -2 -13.0\n")

    def test_additional_arith(self):
        self.sent.register_code(jtc.more_arith)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "256 4\n")

    def test_compare(self):
        self.sent.register_code(jtc.compare)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(), "false true true false true false true\n"
        )

    def test_logical(self):
        self.sent.register_code(jtc.logical)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(), "true false false true false true false true\n"
        )

    def test_assignments(self):
        self.sent.register_code(jtc.assignments)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "8\n16\n36\n36.0\n-18.0\n")

    def test_if_stmt(self):
        self.sent.register_code(jtc.if_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "Hello!\n")

    def test_else_stmt(self):
        self.sent.register_code(jtc.else_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "A is not equal to B\n")

    def test_elif_stmt(self):
        self.sent.register_code(jtc.elif_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "A is one less than B\n")

    def test_for_stmt(self):
        self.sent.register_code(jtc.for_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            "Hello 0 times!\nHello 1 times!\nHello 2 times!\n"
            "Hello 3 times!\nHello 4 times!\nHello 5 times!\n"
            "Hello 6 times!\nHello 7 times!\nHello 8 times!\n"
            "Hello 9 times!\n",
        )

    def test_while_stmt(self):
        self.sent.register_code(jtc.while_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            "Hello 5 times!\nHello 4 times!\nHello 3 times!\n"
            "Hello 2 times!\nHello 1 times!\n",
        )

    def test_break_stmt(self):
        self.sent.register_code(jtc.break_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            "Hello 0 times!\nHello 1 times!\nHello 2 times!\n"
            "Hello 3 times!\nHello 4 times!\nHello 5 times!\n"
            "Hello 6 times!\n",
        )

    def test_continue_stmt(self):
        self.sent.register_code(jtc.continue_stmt)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            "Hello 5 times!\nHello 4 times!\n" "Hello 2 times!\nHello 1 times!\n",
        )

    def test_continue_stmt2(self):
        self.sent.register_code(jtc.continue_stmt2)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            "hello 9\nhello 8\n" "hello 7\nhello 6\nhello 5\n",
        )

    def test_destroy_disconnect(self):
        self.sent.register_code(jtc.destroy_disconn)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        out = self.new_stdout.getvalue()
        self.assertEqual(out.count('"'), 10)

    def test_array_assign(self):
        self.sent.register_code(jtc.array_assign)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            "[[0, 0], [0, 0]]\n"
            "[[1, 1], [0, 0]]\n"
            "[[1, 2], [3, 4]]\n"
            "[[1, 2], [1, 2]]\n",
        )

    def test_md_array_assign(self):
        self.sent.register_code(jtc.array_md_assign)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(), "[[1, 2], [3, 4]]\n" "[[1, 1], [3, 4]]\n"
        )

    def test_dereference(self):
        self.sent.register_code(jtc.dereference)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue()[:9], "urn:uuid:")

    def test_pre_post_walk(self):
        self.sent.register_code(jtc.pre_post_walking)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "count: 8\n")

    def test_pre_post_walk_disengage(self):
        self.sent.register_code(jtc.pre_post_walking_dis)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "count: 6\n")

    def test_length(self):
        self.sent.register_code(jtc.length)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "3\n3\n")

    def test_sort_by_col(self):
        self.sent.register_code(jtc.sort_by_col)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            '[["b", 333], ["c", 245], ["a", 56]]\n'
            '[["a", 56], ["b", 333], ["c", 245]]\n'
            '[["c", 245], ["b", 333], ["a", 56]]\n'
            '[["a", 56], ["c", 245], ["b", 333]]\n'
            '[["b", 333], ["c", 245], ["a", 56]]\n',
        )

    def test_list_remove_element(self):
        self.sent.register_code(jtc.list_remove)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            '[["b", 333], ["c", 245], ["a", 56]]\n'
            '[["b", 333], ["a", 56]]\n[["b", 333]]\n',
        )

    def test_can_action(self):
        self.sent.register_code(jtc.can_action)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "56 7\n" "56 8\n")

    def test_can_action_param(self):
        self.sent.register_code(jtc.can_action_params)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(), "43 7\n" "43 8\n" "48 7\n" "48 8\n"
        )

    def test_cross_scope_report(self):
        self.sent.register_code(jtc.cross_scope_report)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertIn(56, gen_walker.report)
        self.assertIn(8, gen_walker.report)
        self.assertEqual(self.new_stdout.getvalue(), "56 7\n" "56 8\n")

    def test_has_private(self):
        self.sent.register_code(jtc.has_private)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        print(gen_walker.report)
        self.assertIn("'context': {'apple': 12, 'grape': 1", self.new_stdout.getvalue())

    def test_array_idx_of_expr(self):
        self.sent.register_code(jtc.array_idx_of_expr)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(self.new_stdout.getvalue(), "3\n1\n")

    def test_dict_assign(self):
        self.sent.register_code(jtc.dict_assign)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            '{"three": 3, "four": 4}\n'
            '{"three": 3, "four": 55}\n'
            '{"one": 1, "two": 2}\n2\n',
        )

    def test_dict_md_assign(self):
        self.sent.register_code(jtc.dict_md_assign)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            '{"one": {"inner": 44}, "two": 2}\n' '{"inner": 2}\n2\n',
        )

    def test_dict_keys(self):
        self.sent.register_code(jtc.dict_keys)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            '{"one": {"inner": 44}, "two": 2}\n' '{"inner": 2}\n2\n',
        )

    def test_cond_dict_keys(self):
        self.sent.register_code(jtc.cond_dict_keys)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertEqual(
            self.new_stdout.getvalue(),
            '{"one": {"inner": 44}, "two": 2}\n' "is here\n" "also not here\n",
        )

    def test_vector_softmax(self):
        self.sent.register_code(jtc.soft_max)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertTrue(self.new_stdout.getvalue().startswith("[0.836018"))

    def test_book_fam_example(self):
        self.sent.register_code(jtc.fam_example)
        gen_walker = self.sent.run_architype("create_fam")
        gen_walker.prime(self.gph)
        gen_walker.run()
        self.assertIn("I didn't do any of the hard work.\n", self.new_stdout.getvalue())

    def test_book_visitor_preset(self):
        self.sent.register_code(jtc.visitor_preset)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        outsplit = self.new_stdout.getvalue().split("\n")
        self.assertIn("from", outsplit[0])
        self.assertIn("setter", outsplit[0])
        self.assertIn("walker", outsplit[0])
        self.assertIn("init", outsplit[1])
        self.assertIn("walker", outsplit[1])
        self.assertIn("init only", outsplit[2])
        self.assertIn('"name": "init"', outsplit[2])

    def test_book_visitor_local_aciton(self):
        self.sent.register_code(jtc.visitor_local_aciton)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        outsplit = self.new_stdout.getvalue().split("\n")
        self.assertIn('"byear": null', outsplit[0])
        self.assertIn("to 1995: {", outsplit[1])
        self.assertIn("setter", outsplit[2])
        self.assertIn('"byear": "1995-01-01"', outsplit[3])
        self.assertIn('"name": "init"', outsplit[4])

    def test_book_copy_assign_to_edge(self):
        self.sent.register_code(jtc.copy_assign_to_edge)
        gen_walker = self.sent.run_architype("init")
        gen_walker.prime(self.gph)
        gen_walker.run()
        outsplit = self.new_stdout.getvalue().split("\n")
        self.assertIn('"Josh", "age": 32', outsplit[1])
        self.assertIn("college", outsplit[2])
        self.assertIn('"Jane", "age": 30', outsplit[3])
        self.assertIn("sister", outsplit[4])
        self.assertIn('"Josh", "age": 32', outsplit[5])
        self.assertIn("college", outsplit[6])
        self.assertIn('"Jane", "age": 30', outsplit[7])
        self.assertIn("sister", outsplit[8])
