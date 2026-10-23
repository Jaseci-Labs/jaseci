"""The public API must reject misuse through Jac's actual static checker."""
from pathlib import Path
import os
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]


class StaticTypes(unittest.TestCase):
    def test_positive_example_and_module(self):
        result = subprocess.run([sys.executable, '-m', 'jaclang', 'check',
                                 'jac/jaclang/sql.jac', 'jac/examples/sql/typed_sql.jac'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('2 passed', result.stdout+result.stderr)

    def test_all_bad_calls_are_rejected_at_their_lines(self):
        fixture = ROOT/'jac/tests/sql/fixtures/invalid_calls.jac'
        result = subprocess.run([sys.executable, '-m', 'jaclang', 'check', str(fixture)],
                                cwd=ROOT, capture_output=True, text=True)
        output=result.stdout+result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        lines={int(x) for x in re.findall(r'invalid_calls\.jac:(\d+):\d+',output)}
        self.assertEqual(lines, {7,8,9,10,11,12,13,14,17,18,19}, output)
        self.assertEqual(output.count('error[E1053]'),11,output)
