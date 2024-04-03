from app import sum
import unittest


class TestApp(unittest.TestCase):
    def test_sum(self):
        x = ""
        y = ""

        self.assertEqual(sum(1, 2), 3)
        self.assertEqual(sum(0, 0), 0)
        self.assertEqual(sum(-1, 1), 0)


if __name__ == "__main__":
    unittest.main()
