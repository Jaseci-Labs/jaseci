import unittest

# Global variables
r, x, y, z = 5, 10, 5, 5


def foo(a: float) -> float:
    """Function that multiplies a by 2."""
    return a * 2


# Unit Tests
class TestShapesFunctions(unittest.TestCase):
    def test_1(self) -> None:
        """Test case for foo(r) should be approximately equal to x."""
        result = foo(r)
        self.assertAlmostEqual(
            result, x, places=2, msg=f"foo({r}) should be {x}, but got {result}"
        )

    def test_2(self) -> None:
        """Test case for y should be equal to z."""
        self.assertEqual(y, z, msg=f"Expected y to be {z}, but got {y}")

    def test_3(self) -> None:
        """Test case that intentionally fails (for demonstration purposes)."""
        self.assertEqual(
            35,
            4,
            msg="This test is intentionally designed to fail for demonstration purposes.",
        )


def run_tests():
    """Function to run the unit tests."""
    unittest.main()


if __name__ == "__main__":
    run_tests()
