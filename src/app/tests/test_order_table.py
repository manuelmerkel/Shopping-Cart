import unittest

from routes.admin import get_dynamic_table
from routes.user import profile_home_blueprint


class TestOrderTable(unittest.TestCase):

    def test_empty_table(self):
        test_input = []
        dynamic_table = get_dynamic_table(test_input)

        self.assertEqual([], dynamic_table)

    def test_one_order(self):
        test_input = [
            ["1", "1", "A: Test Product"],
            ["2", "1", "Z: Test Product"],
            ["3", "1", "C: Test Product"],
            ["4", "1", "B: Test Product"],
            ["5", "1", "B: Test Product"]
        ]

        dynamic_table = get_dynamic_table(test_input)

        expected_outcome = [
            ["Order ID", "A: Test Product", "B: Test Product", "C: Test Product", "Z: Test Product"],
            ["1", "1", "2", "1", "1"]
        ]
        self.assertEqual(expected_outcome, dynamic_table)

    def test_multiple_orders(self):
        test_input = [
            ["1", "1", "A: Test Product"],
            ["2", "3", "A: Test Product"],
            ["3", "2", "C: Test Product"],
            ["4", "7", "Z: Test Product"],
            ["5", "1", "B: Test Product"],
            ["5", "1", "C: Test Product"],
            ["5", "2", "C: Test Product"],
            ["5", "7", "A: Test Product"]
        ]

        dynamic_table = get_dynamic_table(test_input)

        expected_outcome = [
            ["Order ID", "A: Test Product", "B: Test Product", "C: Test Product", "Z: Test Product"],
            ["1", "1", "1", "1", "0"],
            ["2", "0", "0", "2", "0"],
            ["3", "1", "0", "0", "0"],
            ["7", "1", "0", "0", "1"]
        ]
        self.assertEqual(expected_outcome, dynamic_table)

    def test_multiple_orders_2(self):
        test_input = [
            ["1", "12", "B: Test Product"],
            ["2", "12", "B: Test Product"],
            ["3", "12", "B: Test Product"],
            ["4", "1", "A: Test Product"],
            ["5", "1", "A: Test Product"]
        ]

        dynamic_table = get_dynamic_table(test_input)

        expected_outcome = [
            ["Order ID", "A: Test Product", "B: Test Product"],
            ["1", "2", "0"],
            ["12", "0", "3"]
        ]

        self.assertEqual(expected_outcome, dynamic_table)

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
