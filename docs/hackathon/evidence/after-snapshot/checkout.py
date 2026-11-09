"""Checkout totals in integer cents. Free shipping starts at a $50 original subtotal."""
def total(subtotal_cents, discount_percent):
    discounted = subtotal_cents * (100 - discount_percent) // 100
    shipping = 0 if subtotal_cents >= 5000 else 599
    return discounted + shipping
