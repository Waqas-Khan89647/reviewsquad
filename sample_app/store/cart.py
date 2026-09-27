"""Shopping cart. All money is stored as integer cents."""
from dataclasses import dataclass, field
from typing import List

FREE_DELIVERY_THRESHOLD_CENTS = 5000
DELIVERY_FEE_CENTS = 499


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


def create_cart(items=None):
    """Create and return a Cart pre-populated with the given items.

    Args:
        items: Optional list of (name, price_cents, quantity) tuples.

    Returns:
        A new Cart instance.
    """
    if items is None:
        items = []
    cart = Cart()
    for name, price, qty in items:
        cart.add_item(name, price, qty)
    return cart


def total_cents(cart, coupon_code=None):
    """Return the total to charge in cents, including any delivery fee.

    A delivery fee of DELIVERY_FEE_CENTS is added when the order subtotal
    is below FREE_DELIVERY_THRESHOLD_CENTS. An optional coupon_code is
    applied before the threshold check.

    Args:
        cart: A Cart instance.
        coupon_code: Optional coupon code string.

    Returns:
        Total amount in integer cents.
    """
    from .coupons import apply_coupon

    total = apply_coupon(cart, coupon_code) if coupon_code else cart.subtotal_cents()
    if total < FREE_DELIVERY_THRESHOLD_CENTS:
        total += DELIVERY_FEE_CENTS
    return total