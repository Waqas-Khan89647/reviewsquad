import datetime

import pytest

from store.cart import Cart, FREE_DELIVERY_THRESHOLD_CENTS, DELIVERY_FEE_CENTS, create_cart, total_cents
from store.coupons import add_coupon


# ---------------------------------------------------------------------------
# Existing Cart tests (unchanged)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# create_cart
# ---------------------------------------------------------------------------

def test_create_cart_empty():
    cart = create_cart()
    assert cart.subtotal_cents() == 0


def test_create_cart_with_items():
    cart = create_cart([("mug", 500, 2), ("pen", 100, 1)])
    assert cart.subtotal_cents() == 1100


def test_create_cart_does_not_mutate_caller_list():
    original = [("mug", 500, 1)]
    create_cart(original)
    assert original == [("mug", 500, 1)]


def test_create_cart_none_default_does_not_accumulate():
    """Calling create_cart() twice with no args must return independent carts."""
    cart1 = create_cart()
    cart1.add_item("x", 100)
    cart2 = create_cart()
    assert cart2.subtotal_cents() == 0


# ---------------------------------------------------------------------------
# total_cents
# ---------------------------------------------------------------------------

def test_total_cents_adds_delivery_fee_below_threshold():
    cart = Cart()
    cart.add_item("item", FREE_DELIVERY_THRESHOLD_CENTS - 1)
    assert total_cents(cart) == FREE_DELIVERY_THRESHOLD_CENTS - 1 + DELIVERY_FEE_CENTS


def test_total_cents_no_delivery_fee_at_threshold():
    cart = Cart()
    cart.add_item("item", FREE_DELIVERY_THRESHOLD_CENTS)
    assert total_cents(cart) == FREE_DELIVERY_THRESHOLD_CENTS


def test_total_cents_no_delivery_fee_above_threshold():
    cart = Cart()
    cart.add_item("item", FREE_DELIVERY_THRESHOLD_CENTS + 1)
    assert total_cents(cart) == FREE_DELIVERY_THRESHOLD_CENTS + 1


def test_total_cents_with_valid_coupon():
    add_coupon("CART10", 10, datetime.date.today() + datetime.timedelta(days=1))
    cart = Cart()
    cart.add_item("item", FREE_DELIVERY_THRESHOLD_CENTS)
    # 5000 - 500 = 4500; below threshold so delivery fee added
    assert total_cents(cart, coupon_code="CART10") == 4500 + DELIVERY_FEE_CENTS


def test_total_cents_without_coupon_uses_subtotal():
    cart = Cart()
    cart.add_item("item", 6000)
    assert total_cents(cart) == 6000