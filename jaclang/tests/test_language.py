"""Test Jac language generally."""

import io
import os
import pickle
import sys
import sysconfig


import jaclang.compiler.passes.main as passes
from jaclang import jac_import
from jaclang.cli import cli
from jaclang.compiler.compile import jac_file_to_pass, jac_pass_to_pass, jac_str_to_pass
from jaclang.compiler.passes.main.schedules import py_code_gen_typed
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.settings import settings
from jaclang.utils.test import TestCase


class JacLanguageTests(TestCase):
    """Test pass module."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_sub_abilities(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.fixture_abs_path("sub_abil_sep.jac"))  # type: ignore

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertEqual(
            "Hello, world!\n" "I'm a ninja Myca!\n",
            stdout_value,
        )

    def test_sub_abilities_multi(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the function
        cli.run(self.fixture_abs_path("sub_abil_sep_multilev.jac"))  # type: ignore

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()

        # Assertions or verifications
        self.assertEqual(
            "Hello, world!\n" "I'm a ninja Myca!\n",
            stdout_value,
        )

    def test_simple_jac_red(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import(
            "micro.simple_walk", base_path=self.fixture_abs_path("../../../examples/")
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            stdout_value,
            "Value: -1\nValue: 0\nValue: 1\nValue: 2\nValue: 3\nValue: 4"
            "\nValue: 5\nValue: 6\nValue: 7\nFinal Value: 8\nDone walking.\n",
        )

    def test_guess_game(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("guess_game", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            stdout_value,
            "Too high!\nToo low!\nToo high!\nCongratulations! You guessed correctly.\n",
        )

    def test_chandra_bugs(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("chandra_bugs", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            stdout_value,
            "<link href='{'new_val': 3, 'where': 'from_foo'} rel='stylesheet'\nTrue\n",
        )

    def test_chandra_bugs2(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("chandra_bugs2", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            stdout_value,
            "{'apple': None, 'pineapple': None}\n"
            "This is a long\n"
            "        line of code.\n"
            "{'a': 'apple', 'b': 'ball', 'c': 'cat', 'd': 'dog', 'e': 'elephant'}\n",
        )

    # TODO: Move these tests to mtllm repo
    # def test_with_llm_function(self) -> None:
    #     """Parse micro jac file."""
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output
    #     jac_import("with_llm_function", base_path=self.fixture_abs_path("./"))
    #     sys.stdout = sys.__stdout__
    #     stdout_value = captured_output.getvalue()
    #     self.assertIn("{'temperature': 0.7}", stdout_value)
    #     self.assertIn("Emoji Representation (str)", stdout_value)
    #     self.assertIn('Text Input (input) (str) = "Lets move to paris"', stdout_value)
    #     self.assertIn(
    #         ' = [{"input": "I love tp drink pina coladas"',
    #         stdout_value,
    #     )

    # def test_with_llm_method(self) -> None:
    #     """Parse micro jac file."""
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output
    #     jac_import("with_llm_method", base_path=self.fixture_abs_path("./"))
    #     sys.stdout = sys.__stdout__
    #     stdout_value = captured_output.getvalue()
    #     self.assertIn("[Reasoning] <Reason>", stdout_value)
    #     self.assertIn("(Enum) eg:- Personality.EXTROVERT ->", stdout_value)
    #     self.assertIn(
    #         "Personality Index of a Person (PersonalityIndex) (class) eg:- "
    #         "PersonalityIndex(index=int) -> Personality Index (index) (int)",
    #         stdout_value,
    #     )
    #     self.assertIn(
    #         "Personality of the Person (dict[Personality,PersonalityIndex])",
    #         stdout_value,
    #     )
    #     self.assertIn(
    #         'Diary Entries (diary_entries) (list[str]) = ["I won noble prize in '
    #         'Physics", "I am popular for my theory of relativity"]',
    #         stdout_value,
    #     )

    # def test_with_llm_lower(self) -> None:
    #     """Parse micro jac file."""
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output
    #     jac_import("with_llm_lower", base_path=self.fixture_abs_path("./"))
    #     sys.stdout = sys.__stdout__
    #     stdout_value = captured_output.getvalue()
    #     self.assertIn("[Reasoning] <Reason>", stdout_value)
    #     self.assertIn(
    #         'Name of the Person (name) (str) = "Oppenheimer"',
    #         stdout_value,
    #     )
    #     self.assertIn(
    #         "Person (Person) (obj) eg:- Person(full_name=str, yod=int, personality"
    #         "=Personality) -> Fullname of the Person (full_name) (str), Year of Death"
    #         " (yod) (int), Personality of the Person (personality) (Personality)",
    #         stdout_value,
    #     )
    #     self.assertIn(
    #         "J. Robert Oppenheimer was a Introvert person who died in 1967",
    #         stdout_value,
    #     )

    # def test_with_llm_type(self) -> None:
    #     """Parse micro jac file."""
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output
    #     jac_import("with_llm_type", base_path=self.fixture_abs_path("./"))
    #     sys.stdout = sys.__stdout__
    #     stdout_value = captured_output.getvalue()
    #     self.assertIn("14/03/1879", stdout_value)
    #     self.assertNotIn(
    #         'University (University) (obj) = type(__module__="with_llm_type", __doc__=None, '
    #         "_jac_entry_funcs_`=[`], _jac_exit_funcs_=[], __init__=function(__wrapped__=function()))",
    #         stdout_value,
    #     )
    #     desired_output_count = stdout_value.count(
    #         "Person(name='Jason Mars', dob='1994-01-01', age=30)"
    #     )
    #     self.assertEqual(desired_output_count, 2)

    # def test_with_llm_vision(self) -> None:
    #     """Test MTLLLM Vision Implementation."""
    #     try:
    #         captured_output = io.StringIO()
    #         sys.stdout = captured_output
    #         jac_import("with_llm_vision", base_path=self.fixture_abs_path("./"))
    #         sys.stdout = sys.__stdout__
    #         stdout_value = captured_output.getvalue()
    #         self.assertIn(
    #             "{'type': 'text', 'text': '\\n[System Prompt]\\n", stdout_value[:500]
    #         )
    #         self.assertNotIn(
    #             " {'type': 'text', 'text': 'Image of the Question (question_img) (Image) = '}, "
    #             "{'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQAB",
    #             stdout_value[:500],
    #         )
    #     except Exception:
    #         self.skipTest("This test requires Pillow to be installed.")

    def test_ignore(self) -> None:
        """Parse micro jac file."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("ignore_dup", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.split("\n")[0].count("here"), 10)
        self.assertEqual(stdout_value.split("\n")[1].count("here"), 5)

    def test_dataclass_hasability(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("hashcheck_dup", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.count("check"), 2)

    def test_arith_precedence(self) -> None:
        """Basic precedence test."""
        prog = jac_str_to_pass("with entry {print(4-5-4);}", "test.jac")
        captured_output = io.StringIO()
        sys.stdout = captured_output
        exec(compile(prog.ir.gen.py_ast[0], "test.py", "exec"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value, "-5\n")

    def test_need_import(self) -> None:
        """Test importing python."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("needs_import", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("<module 'pyfunc' from", stdout_value)

    def test_filter_compr(self) -> None:
        """Testing filter comprehension."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import(
            "reference.special_comprehensions",
            base_path=self.fixture_abs_path("../../../examples/"),
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("TestObj", stdout_value)

    def test_gen_dot_bubble(self) -> None:
        """Test the dot gen of nodes and edges of bubblesort."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("gendot_bubble_sort", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn(
            '[label="inner_node(main=5, sub=2)"];',
            stdout_value,
        )

    def test_assign_compr(self) -> None:
        """Test assign_compr."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("assign_compr_dup", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(
            "[MyObj(apple=5, banana=7), MyObj(apple=5, banana=7)]\n",
            stdout_value,
        )

    def test_semstr(self) -> None:
        """Test semstring."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("semstr", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertNotIn("Error", stdout_value)

    def test_raw_bytestr(self) -> None:
        """Test raw string and byte string."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("raw_byte_string", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.count(r"\\\\"), 2)
        self.assertEqual(stdout_value.count("<class 'bytes'>"), 3)

    def test_deep_imports(self) -> None:
        """Parse micro jac file."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("deep_import", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.split("\n")[0], "one level deeperslHello World!")

    def test_deep_outer_imports_one(self) -> None:
        """Parse micro jac file."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import(
            "deep.deeper.deep_outer_import", base_path=self.fixture_abs_path("./")
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("one level deeperslHello World!", stdout_value)
        self.assertIn("module 'pyfunc' from ", stdout_value)

    def test_deep_outer_imports_from_loc(self) -> None:
        """Parse micro jac file."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        os.chdir(self.fixture_abs_path("./deep/deeper/"))
        cli.run("deep_outer_import.jac")
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("one level deeperslHello World!", stdout_value)
        self.assertIn("module 'pyfunc' from ", stdout_value)

    # def test_second_deep_outer_imports(self) -> None:
    #     """Parse micro jac file."""
    #     Jac.get_root()._jac_.edges.clear()
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output
    #     jac_import(
    #         "deep.deeper.deep_outer_import2", base_path=self.fixture_abs_path("./")
    #     )
    #     sys.stdout = sys.__stdout__
    #     stdout_value = captured_output.getvalue()
    #     self.assertIn("one level deeperslHello World!", stdout_value)
    #     self.assertIn("module 'pyfunc' from ", stdout_value)

    def test_has_lambda_goodness(self) -> None:
        """Test has lambda_goodness."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("has_goodness", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.split("\n")[0], "mylist:  [1, 2, 3]")
        self.assertEqual(stdout_value.split("\n")[1], "mydict:  {'a': 2, 'b': 4}")

    def test_conn_assign_on_edges(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("edge_ops", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("[(3, 5), (14, 1), (5, 1)]", stdout_value)
        self.assertIn("10\n", stdout_value)
        self.assertIn("12\n", stdout_value)

    def test_disconnect(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("disconn", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue().split("\n")
        self.assertIn("c(cc=0)", stdout_value[0])
        self.assertIn("c(cc=1)", stdout_value[0])
        self.assertIn("c(cc=2)", stdout_value[0])
        self.assertIn("True", stdout_value[2])
        self.assertIn("[]", stdout_value[3])
        self.assertIn(
            "['GenericEdge', 'GenericEdge', 'GenericEdge']",
            stdout_value[5],
        )

    def test_simple_archs(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("simple_archs", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.split("\n")[0], "1 2 0")
        self.assertEqual(stdout_value.split("\n")[1], "0")

    def test_edge_walk(self) -> None:
        """Test walking through edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("edges_walk", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("creator()\n", stdout_value)
        self.assertIn("[node_a(val=12)]\n", stdout_value)
        self.assertIn("node_a(val=1)", stdout_value)
        self.assertIn("node_a(val=2)", stdout_value)
        self.assertIn("[node_a(val=42), node_a(val=42)]\n", stdout_value)

    def test_impl_grab(self) -> None:
        """Test walking through edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("impl_grab", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("1.414", stdout_value)

    def test_tuple_of_tuple_assign(self) -> None:
        """Test walking through edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("tuplytuples", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn(
            "a apple b banana a apple b banana a apple b banana a apple b banana",
            stdout_value,
        )

    def test_deferred_field(self) -> None:
        """Test walking through edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("deferred_field", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn(
            "5 15",
            stdout_value,
        )

    def test_gen_dot_builtin(self) -> None:
        """Test the dot gen of nodes and edges as a builtin."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("builtin_dotgen", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        print(stdout_value)
        self.assertEqual(stdout_value.count("True"), 14)

    def test_with_contexts(self) -> None:
        """Test walking through edges."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("with_context", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("im in", stdout_value)
        self.assertIn("in the middle", stdout_value)
        self.assertIn("im out", stdout_value)
        self.assertIn(
            "{'apple': [1, 2, 3], 'banana': [1, 2, 3], 'cherry': [1, 2, 3]}",
            stdout_value,
        )

    def test_typed_filter_compr(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import(
            "micro.typed_filter_compr",
            base_path=self.fixture_abs_path("../../../examples/"),
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn(
            "[MyObj(a=0), MyObj2(a=2), MyObj(a=1), "
            "MyObj2(a=3), MyObj(a=2), MyObj(a=3)]\n",
            stdout_value,
        )
        self.assertIn("[MyObj(a=0), MyObj(a=1), MyObj(a=2)]\n", stdout_value)

    def test_edge_node_walk(self) -> None:
        """Test walking through edges and nodes."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("edge_node_walk", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("creator()\n", stdout_value)
        self.assertIn("[node_a(val=12)]\n", stdout_value)
        self.assertIn("node_a(val=1)", stdout_value)
        self.assertIn("node_a(val=2)", stdout_value)
        self.assertIn("[node_b(val=42), node_b(val=42)]\n", stdout_value)

    def test_annotation_tuple_issue(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        mypass = jac_file_to_pass(self.fixture_abs_path("./slice_vals.jac"))
        self.assertIn("Annotated[Str, INT, BLAH]", mypass.ir.gen.py)
        self.assertIn("tuple[int, Optional[type], Optional[tuple]]", mypass.ir.gen.py)

    def test_impl_decl_resolution_fix(self) -> None:
        """Test walking through edges and nodes."""
        Jac.get_root()._jac_.edges.clear()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("mtest", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("2.0\n", stdout_value)

    def test_registry(self) -> None:
        """Test Jac registry feature."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("registry", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertNotIn("Error", stdout_value)

        with open(
            os.path.join(
                self.fixture_abs_path("./"), "__jac_gen__", "registry.registry.pkl"
            ),
            "rb",
        ) as f:
            registry = pickle.load(f)

        self.assertEqual(len(registry.registry), 3)
        self.assertEqual(len(list(registry.registry.items())[0][1]), 10)
        self.assertEqual(list(registry.registry.items())[1][0].scope, "Person")

    def test_enum_inside_arch(self) -> None:
        """Test Enum as member stmt."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("enum_inside_archtype", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual("2\n", stdout_value)

    def test_needs_import_1(self) -> None:
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = True
        file_name = os.path.join(self.fixture_abs_path("./"), "needs_import_1.jac")
        from jaclang.compiler.passes.main.schedules import py_code_gen
        import jaclang.compiler.absyntree as ast

        ir = jac_file_to_pass(file_name, schedule=py_code_gen).ir
        self.assertEqual(len(ir.get_all_sub_nodes(ast.Architype)), 7)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("needs_import_1", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_1 imported", stdout_value)
        settings.py_raise = False

    def test_pyfunc_1(self) -> None:
        """Test py ast to Jac ast conversion."""
        from jaclang.compiler.passes.main import PyastBuildPass
        import jaclang.compiler.absyntree as ast
        import ast as py_ast

        py_out_path = os.path.join(self.fixture_abs_path("./"), "pyfunc_1.py")
        with open(py_out_path) as f:
            output = PyastBuildPass(
                input_ir=ast.PythonModuleAst(
                    py_ast.parse(f.read()), mod_path=py_out_path
                ),
            ).ir.unparse()
        # print(output)
        self.assertIn("can greet2(**kwargs: Any)", output)
        self.assertEqual(output.count("with entry {"), 13)
        self.assertIn(
            '"""Enum for shape types"""\nenum ShapeType{ CIRCLE = "Circle",\n',
            output,
        )
        self.assertIn(
            "UNKNOWN = \"Unknown\",\n::py::\nprint('hello')\n::py::\n }", output
        )
        self.assertIn('assert x == 5 , "x should be equal to 5" ;', output)
        self.assertIn("if not x == y {", output)
        self.assertIn("can greet2(**kwargs: Any) {", output)
        self.assertIn("squares_dict = {x: (x ** 2)  for x in numbers};", output)
        self.assertIn(
            '\n\n@ my_decorator \n can say_hello() {\n    """Say hello""" ; ', output
        )

    def test_needs_import_2(self) -> None:
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = True
        file_name = os.path.join(self.fixture_abs_path("./"), "needs_import_2.jac")
        from jaclang.compiler.passes.main.schedules import py_code_gen
        import jaclang.compiler.absyntree as ast

        ir = jac_file_to_pass(file_name, schedule=py_code_gen).ir
        self.assertEqual(len(ir.get_all_sub_nodes(ast.Architype)), 5)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("needs_import_2", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_2 imported", stdout_value)
        self.assertEqual(stdout_value.count("<class 'bytes'>"), 3)
        settings.py_raise = False

    def test_pyfunc_2(self) -> None:
        """Test py ast to Jac ast conversion."""
        from jaclang.compiler.passes.main import PyastBuildPass
        import jaclang.compiler.absyntree as ast
        import ast as py_ast

        py_out_path = os.path.join(self.fixture_abs_path("./"), "pyfunc_2.py")
        with open(py_out_path) as f:
            output = PyastBuildPass(
                input_ir=ast.PythonModuleAst(
                    py_ast.parse(f.read()), mod_path=py_out_path
                ),
            ).ir.unparse()
        self.assertIn("class X {\n    with entry {\n        a_b = 67;", output)
        self.assertIn("br = b'Hello\\\\\\\\nWorld'", output)
        self.assertIn("class Circle {\n    can init(radius: float", output)

    def test_needs_import_3(self) -> None:
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = True
        file_name = os.path.join(self.fixture_abs_path("./"), "needs_import_3.jac")
        from jaclang.compiler.passes.main.schedules import py_code_gen
        import jaclang.compiler.absyntree as ast

        ir = jac_file_to_pass(file_name, schedule=py_code_gen).ir
        self.assertEqual(len(ir.get_all_sub_nodes(ast.Architype)), 6)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("needs_import_3", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("pyfunc_3 imported", stdout_value)
        settings.py_raise = False

    def test_pyfunc_3(self) -> None:
        """Test py ast to Jac ast conversion."""
        from jaclang.compiler.passes.main import PyastBuildPass
        import jaclang.compiler.absyntree as ast
        import ast as py_ast

        py_out_path = os.path.join(self.fixture_abs_path("./"), "pyfunc_3.py")
        with open(py_out_path) as f:
            output = PyastBuildPass(
                input_ir=ast.PythonModuleAst(
                    py_ast.parse(f.read()), mod_path=py_out_path
                ),
            ).ir.unparse()
        self.assertIn("if 0 <= x<= 5 {", output)
        self.assertIn("  case _:\n", output)
        self.assertIn(" case Point(x = int(_), y = 0):\n", output)
        self.assertIn("class Sample {\n    can init", output)

    def test_py_kw_as_name_disallowed(self) -> None:
        """Basic precedence test."""
        prog = jac_str_to_pass("with entry {print.is.not.True(4-5-4);}", "test.jac")
        self.assertIn("Python keyword is used as name", str(prog.errors_had[0].msg))

    def test_double_format_issue(self) -> None:
        """Basic precedence test."""
        prog = jac_str_to_pass("with entry {print(hello);}", "test.jac")
        prog.ir.unparse()
        before = prog.ir.format()
        prog.ir.format()
        prog.ir.format()
        after = prog.ir.format()
        self.assertEqual(before, after)

    def test_type_fuse_expr(self) -> None:
        """Basic test for pass."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.tool(
            "ir",
            [
                "ast",
                self.fixture_abs_path(
                    "../../../examples/reference/collection_values.jac"
                ),
            ],
        )

        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn(
            "builtins.dict[builtins.int, builtins.int]",
            stdout_value,
        )
        self.assertIn(
            "typing.Generator[builtins.int, None, None]",
            stdout_value,
        )

    def test_inherit_check(self) -> None:
        """Test py ast to Jac ast conversion output."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("inherit_check", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual("I am in b\nI am in b\nwww is also in b\n", stdout_value)

    def test_tuple_unpack(self) -> None:
        """Test tuple unpack."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("tupleunpack", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue().split("\n")
        self.assertIn("1", stdout_value[0])
        self.assertIn("[2, 3, 4]", stdout_value[1])

    def test_try_finally(self) -> None:
        """Test try finally."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("try_finally", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue().split("\n")
        self.assertIn("try block", stdout_value[0])
        self.assertIn("finally block", stdout_value[1])
        self.assertIn("try block", stdout_value[2])
        self.assertIn("else block", stdout_value[3])
        self.assertIn("finally block", stdout_value[4])

    def test_arithmetic_bug(self) -> None:
        """Test arithmetic bug."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("arithmetic_bug", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue().split("\n")
        self.assertEqual("0.0625", stdout_value[0])
        self.assertEqual("1e-06", stdout_value[1])
        self.assertEqual("1000.000001", stdout_value[2])
        self.assertEqual("78", stdout_value[3])
        self.assertEqual("12", stdout_value[4])

    def test_lambda_expr(self) -> None:
        """Test lambda expr."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("lambda", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue().split("\n")
        self.assertEqual("9", stdout_value[0])
        self.assertEqual("567", stdout_value[1])

    def test_random_check(self) -> None:
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = True

        from jaclang.compiler.passes.main import PyastBuildPass
        import jaclang.compiler.absyntree as ast
        import ast as py_ast

        module_paths = ["random", "tkinter"]
        for module_path in module_paths:
            stdlib_dir = sysconfig.get_paths()["stdlib"]
            file_path = os.path.join(
                stdlib_dir,
                module_path + (".py" if module_path == "random" else "/__init__.py"),
            )
            with open(file_path) as f:
                jac_ast = PyastBuildPass(
                    input_ir=ast.PythonModuleAst(
                        py_ast.parse(f.read()), mod_path=file_path
                    )
                )
            ir = jac_pass_to_pass(jac_ast).ir
            gen_ast = ir.pp()
            if module_path == "random":
                self.assertIn("ModulePath - statistics -", gen_ast)
            else:
                self.assertIn("+-- Name - TclError - Type: No", gen_ast)
        settings.py_raise = False

    def test_deep_py_load_imports(self) -> None:  # we can get rid of this, isn't?
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = True
        file_name = os.path.join(self.fixture_abs_path("./"), "random_check.jac")
        from jaclang.compiler.passes.main.schedules import py_code_gen, PyImportPass

        imp = jac_file_to_pass(file_name, schedule=py_code_gen, target=PyImportPass)
        self.assertEqual(len(imp.import_table), 1)
        settings.py_raise = False

    def test_access_modifier(self) -> None:
        """Test for access tags working."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cli.check(
            self.fixture_abs_path("../../tests/fixtures/access_modifier.jac"),
            print_errs=True,
        )
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn('Can not access private variable "p"', stdout_value)
        self.assertIn('Can not access private variable "privmethod"', stdout_value)
        self.assertIn('Can not access private variable "BankAccount"', stdout_value)
        self.assertNotIn(" Name: ", stdout_value)

    def test_deep_convert(self) -> None:
        """Test py ast to Jac ast conversion output."""
        settings.py_raise = settings.py_raise_deep = True
        file_name = os.path.join(self.fixture_abs_path("./"), "deep_convert.jac")
        from jaclang.compiler.passes.main.schedules import py_code_gen
        import jaclang.compiler.absyntree as ast

        ir = jac_file_to_pass(file_name, schedule=py_code_gen).ir
        jac_ast = ir.pp()
        self.assertIn(' |   +-- String - "Loop compl', jac_ast)
        self.assertEqual(len(ir.get_all_sub_nodes(ast.SubNodeList)), 272)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("deep_convert", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Deep convo is imported", stdout_value)
        settings.py_raise = settings.py_raise_deep = False

    def test_override_walker_inherit(self) -> None:
        """Test py ast to Jac ast conversion output."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("walker_override", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual("baz\nbar\n", stdout_value)

    def test_ds_type_check_pass(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        mypass = jac_file_to_pass(
            self.fixture_abs_path("../../../examples/micro/simple_walk.jac"),
            schedule=py_code_gen_typed,
        )
        self.assertEqual(len(mypass.errors_had), 0)
        self.assertEqual(len(mypass.warnings_had), 0)

    def test_ds_type_check_pass2(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        mypass = jac_file_to_pass(
            self.fixture_abs_path("../../../examples/guess_game/guess_game5.jac"),
            schedule=py_code_gen_typed,
        )
        self.assertEqual(len(mypass.errors_had), 0)
        self.assertEqual(len(mypass.warnings_had), 0)

    def test_self_with_no_sig(self) -> None:  # we can get rid of this, isn't?
        """Test py ast to Jac ast conversion output."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("nosigself", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertEqual(stdout_value.count("5"), 2)

    def test_hash_init_check(self) -> None:  # we can get rid of this, isn't?
        """Test py ast to Jac ast conversion output."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("hash_init_check", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("Test Passed", stdout_value)

    def test_multiline_single_tok(self) -> None:
        """Test conn assign on edges."""
        Jac.get_root()._jac_.edges.clear()
        mypass = jac_file_to_pass(self.fixture_abs_path("byllmissue.jac"))
        self.assertIn("2:5 - 4:8", mypass.ir.pp())

    def test_single_impl_annex(self) -> None:
        """Basic test for pass."""
        mypass = jac_file_to_pass(
            self.fixture_abs_path("../../../examples/manual_code/circle_pure.jac"),
            target=passes.JacImportPass,
        )

        self.assertEqual(mypass.ir.pp().count("AbilityDef - (o)Circle.(c)area"), 1)
        self.assertIsNone(mypass.ir._sym_tab)
        mypass = jac_file_to_pass(
            self.fixture_abs_path("../../../examples/manual_code/circle_pure.jac"),
            target=passes.SymTabBuildPass,
        )
        self.assertEqual(
            len([i for i in mypass.ir.sym_tab.kid if i.name == "circle_pure.impl"]),
            1,
        )

    def test_inherit_baseclass_sym(self) -> None:
        """Basic test for symtable support for inheritance."""
        mypass = jac_file_to_pass(
            self.fixture_abs_path("../../../examples/guess_game/guess_game4.jac"),
            target=passes.DefUsePass,
        )
        table = None
        for i in mypass.ir.sym_tab.kid:
            print(i.name)
            if i.name == "GuessTheNumberGame":
                for j in i.kid:
                    if j.name == "play":
                        table = j
                        break
                break
        self.assertIsNotNone(table)
        self.assertIsNotNone(table.lookup("attempts"))

    def test_edge_expr_not_type(self) -> None:
        """Test importing python."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("edgetypeissue", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("[x()]", stdout_value)
