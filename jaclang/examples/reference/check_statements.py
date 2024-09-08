from __future__ import annotations
from jaclang.plugin.feature import JacFeature as _Jac

a = 5
b = 2


@_Jac.create_test
def test_test1(check) -> None:
    check.assertAlmostEqual(a, 6)


@_Jac.create_test
def test_test2(check) -> None:
    check.assertTrue(a != b)


@_Jac.create_test
def test_test3(check) -> None:
    check.assertIn("d", "abc")


@_Jac.create_test
def test_test4(check) -> None:
    check.assertEqual(a - b, 3)
