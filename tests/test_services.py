import unittest
from services import find_order, evaluate_return

class EcoMarketTests(unittest.TestCase):
    def test_existing_order(self):
        order = find_order("EM-1001")
        self.assertIsNotNone(order)
        self.assertEqual(order["status"], "En tránsito")

    def test_missing_order(self):
        self.assertIsNone(find_order("EM-9999"))

    def test_perishable_not_returnable(self):
        order = find_order("EM-1003")
        result = evaluate_return(order, opened=False)
        self.assertFalse(result["eligible"])

    def test_hygiene_opened_not_returnable(self):
        order = find_order("EM-1002")
        result = evaluate_return(order, opened=True)
        self.assertFalse(result["eligible"])

    def test_textile_returnable(self):
        order = find_order("EM-1010")
        result = evaluate_return(order, opened=False)
        self.assertTrue(result["eligible"])

if __name__ == "__main__":
    unittest.main()
