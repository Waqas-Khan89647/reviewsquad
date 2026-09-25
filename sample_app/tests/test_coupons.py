from store.cart import Cart
from store.coupons import apply_coupon


def test_unknown_coupon_changes_nothing():
    cart = Cart()
    cart.add_item("mug", 1000)
    assert apply_coupon(cart, "NOPE") == 1000
