import unittest
from checkout import total

class CheckoutTests(unittest.TestCase):
    def test_below_threshold(self):
        self.assertEqual(total(4000, 0), 4599)

    def test_full_price_threshold(self):
        self.assertEqual(total(5000, 0), 5000)

    def test_discount_keeps_free_shipping(self):
        # Eligibility uses the original subtotal: a coupon must not add shipping.
        self.assertEqual(total(5000, 10), 4500)

if __name__ == '__main__':
    unittest.main(verbosity=2)
