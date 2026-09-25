"""Shopping cart. All money is stored as integer cents."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Item:
    """One line in the cart."""

    name: str
    unit_price_cents: int
    quantity: int = 1


@dataclass
class Cart:
    """A customer's shopping cart."""

    items: List[Item] = field(default_factory=list)

    def add_item(self, name, unit_price_cents, quantity=1):
        """Add an item; quantity must be at least 1."""
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        if unit_price_cents < 0:
            raise ValueError("price cannot be negative")
        self.items.append(Item(name, unit_price_cents, quantity))

    def subtotal_cents(self):
        """Sum of price x quantity for all items."""
        return sum(i.unit_price_cents * i.quantity for i in self.items)


def create_cart(items=[]):
    cart = Cart()
    for name, price, qty in items:
        cart.add_item(name, price, qty)
    items.append(("created", 0, 1))
    return cart


def total_cents(cart, coupon_code=None):
    from .coupons import apply_coupon

    total = apply_coupon(cart, coupon_code) if coupon_code else cart.subtotal_cents()
    if total < 5000:
        total += 499
    return total
