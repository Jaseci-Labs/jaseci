"""Tests for Integration with Jaclang."""

import io
import sys

from jaclang import jac_import
from jaclang.utils.test import TestCase


class JacLanguageTests(TestCase):
    """Tests for Integration with Jaclang."""

    def setUp(self) -> None:
        """Set up test."""
        return super().setUp()

    def test_with_llm_function(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("with_llm_function", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("{'temperature': 0.7}", stdout_value)
        self.assertIn("Emoji Representation (str)", stdout_value)
        self.assertIn('Text Input (input) (str) = "Lets move to paris"', stdout_value)
        self.assertIn(
            ' = [{"input": "I love tp drink pina coladas"',
            stdout_value,
        )

    def test_with_llm_method(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("with_llm_method", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("[Reasoning] <Reason>", stdout_value)
        self.assertIn(
            "Personality of the Person (Personality) (Enum) eg:- Personality.INTROVERT",
            stdout_value,
        )
        self.assertIn(
            "Personality Index of a Person (PersonalityIndex) (class) eg:- "
            'PersonalityIndex(index="Personality Index":int)',
            stdout_value,
        )
        self.assertIn(
            "Personality of the Person (dict[Personality,PersonalityIndex])",
            stdout_value,
        )
        self.assertIn(
            'Diary Entries (diary_entries) (list[str]) = ["I won noble prize in '
            'Physics", "I am popular for my theory of relativity"]',
            stdout_value,
        )

    def test_with_llm_lower(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("with_llm_lower", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("[Reasoning] <Reason>", stdout_value)
        self.assertIn(
            'Name of the Person (name) (str) = "Oppenheimer"',
            stdout_value,
        )
        self.assertIn(
            'Person (Person) (obj) eg:- Person(full_name="Fullname of the Person":str, '
            'yod="Year of Death":int, personality="Personality of the Person":Personality)',
            stdout_value,
        )
        self.assertIn(
            "J. Robert Oppenheimer was a Introvert person who died in 1967",
            stdout_value,
        )

    def test_with_llm_type(self) -> None:
        """Parse micro jac file."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        jac_import("with_llm_type", base_path=self.fixture_abs_path("./"))
        sys.stdout = sys.__stdout__
        stdout_value = captured_output.getvalue()
        self.assertIn("14/03/1879", stdout_value)
        self.assertNotIn(
            'University (University) (obj) = type(__module__="with_llm_type", __doc__=None, '
            "_jac_entry_funcs_`=[`], _jac_exit_funcs_=[], __init__=function(__wrapped__=function()))",
            stdout_value,
        )
        desired_output_count = stdout_value.count(
            "Person(name='Jason Mars', dob='1994-01-01', age=30)"
        )
        self.assertEqual(desired_output_count, 2)

    def test_with_llm_image(self) -> None:
        """Test MTLLLM Image Implementation."""
        try:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            jac_import("with_llm_image", base_path=self.fixture_abs_path("./"))
            sys.stdout = sys.__stdout__
            stdout_value = captured_output.getvalue()
            self.assertIn(
                "{'type': 'text', 'text': '\\n[System Prompt]\\n", stdout_value[:500]
            )
            self.assertNotIn(
                " {'type': 'text', 'text': 'Image of the Question (question_img) (Image) = '}, "
                "{'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQAB",
                stdout_value[:500],
            )
        except Exception:
            self.skipTest("This test requires Pillow to be installed.")

    def test_with_llm_video(self) -> None:
        """Test MTLLLM Video Implementation."""
        try:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            jac_import("with_llm_video", base_path=self.fixture_abs_path("./"))
            sys.stdout = sys.__stdout__
            stdout_value = captured_output.getvalue()
            self.assertIn(
                "{'type': 'text', 'text': '\\n[System Prompt]\\n", stdout_value[:500]
            )
            self.assertEqual(stdout_value.count("data:image/jpeg;base64"), 4)
        except Exception:
            self.skipTest("This test requires OpenCV to be installed.")
