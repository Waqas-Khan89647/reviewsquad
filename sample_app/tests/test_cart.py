import pytest

from store.cart import Cart


def test_subtotal():
    cart = Cart()
    cart.add_item("mug", 1250, 2)
    cart.add_item("pen", 199)
    assert cart.subtotal_cents() == 2699


def test_quantity_must_be_positive():
    with pytest.raises(ValueError):
        Cart().add_item("mug", 1250, 0)


def test_negative_price_rejected():
    with pytest.raises(ValueError):
        Cart().add_item("mug", -1)
