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
