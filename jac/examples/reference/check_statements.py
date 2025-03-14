from __future__ import annotations
from jaclang import *

a = 5
b = 2


@jac_test
def test_test1(_check) -> None:
    _check.assertAlmostEqual(a, 6)


@jac_test
def test_test2(_check) -> None:
    _check.assertNotEqual(a, b)


@jac_test
def test_test3(_check) -> None:
    _check.assertIn("d", "abc")


@jac_test
def test_test4(_check) -> None:
    _check.assertEqual(a - b, 3)
