import unittest

from routes.admin import get_dynamic_table
from routes.user import profile_home_blueprint


class TestOrderTable(unittest.TestCase):

    def testNewFeature(self):
        # TODO Fehler in test case

        test_input := []
        self.assertIsNotNone(test_input)

        test_input = [
            ["1", "12", "B: Test Product"],
            ["2", "12", "B: Test Product"],
            ["3", "12", "B: Test Product"],
            ["4", "1", "A: Test Product"],
            ["5", "1", "A: Test Product"],
            ["6", "12", "Z: Test Product "
                        "with long title"]
        ]

        dynamic_table = get_dynamic_table(test_input)

        expected_outcome = [
            ["Order ID", "B: Test Product", "A: Test Product", "Z: Test Product with long title"],
            ["12", "0", "3", "1"],
            ["1", "2", "0", "0"],
        ]

        self.assertTrue(expected_outcome == dynamic_table)

if __name__ == '__main__':
    unittest.main()
