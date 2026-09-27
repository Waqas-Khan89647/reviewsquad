import datetime

import pytest

from store.cart import Cart
from store.coupons import COUPONS, add_coupon, apply_coupon, is_valid, rule_allows


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_cart(price_cents=1000):
    cart = Cart()
    cart.add_item("item", price_cents)
    return cart


def _tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)


def _yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)


def _today():
    return datetime.date.today()


# ---------------------------------------------------------------------------
# add_coupon - input validation
# ---------------------------------------------------------------------------

def test_add_coupon_rejects_zero_percent():
    with pytest.raises(ValueError):
        add_coupon("BAD0", 0, _tomorrow())


def test_add_coupon_rejects_over_100_percent():
    with pytest.raises(ValueError):
        add_coupon("BAD101", 101, _tomorrow())


def test_add_coupon_rejects_unknown_rule():
    with pytest.raises(ValueError):
        add_coupon("BADRULE", 10, _tomorrow(), rule="evil_rule")


def test_add_coupon_accepts_boundary_percent():
    add_coupon("EDGE1", 1, _tomorrow())
    add_coupon("EDGE100", 100, _tomorrow())
    assert COUPONS["EDGE1"]["percent"] == 1
    assert COUPONS["EDGE100"]["percent"] == 100


# ---------------------------------------------------------------------------
# is_valid - expiry logic
# ---------------------------------------------------------------------------

def test_is_valid_future_coupon():
    add_coupon("FUTURE", 10, _tomorrow())
    assert is_valid("FUTURE", _today()) is True


def test_is_valid_coupon_expiring_today_is_still_valid():
    add_coupon("TODAY", 10, _today())
    assert is_valid("TODAY", _today()) is True


def test_is_valid_expired_coupon():
    add_coupon("EXPIRED", 10, _yesterday())
    assert is_valid("EXPIRED", _today()) is False


def test_is_valid_unknown_code():
    assert is_valid("DOESNOTEXIST", _today()) is False


# ---------------------------------------------------------------------------
# rule_allows
# ---------------------------------------------------------------------------

def test_rule_allows_always_rule():
    add_coupon("ALWAYS", 10, _tomorrow(), rule="always")
    cart = _make_cart()
    assert rule_allows("ALWAYS", cart) is True


# ---------------------------------------------------------------------------
# apply_coupon - normal cases
# ---------------------------------------------------------------------------

def test_unknown_coupon_changes_nothing():
    cart = _make_cart(1000)
    assert apply_coupon(cart, "NOPE") == 1000


def test_apply_coupon_applies_10_percent_discount():
    add_coupon("TEN", 10, _tomorrow())
    cart = _make_cart(1000)
    # 1000 - 1000*10//100 = 1000 - 100 = 900
    assert apply_coupon(cart, "TEN") == 900


def test_apply_coupon_applies_25_percent_discount():
    add_coupon("QUARTER", 25, _tomorrow())
    cart = _make_cart(2000)
    # 2000 - 2000*25//100 = 2000 - 500 = 1500
    assert apply_coupon(cart, "QUARTER") == 1500


def test_apply_expired_coupon_returns_full_price():
    add_coupon("OLD", 50, _yesterday())
    cart = _make_cart(1000)
    assert apply_coupon(cart, "OLD") == 1000


def test_apply_coupon_expiring_today_is_applied():
    add_coupon("TODAYCPN", 20, _today())
    cart = _make_cart(1000)
    # 1000 - 1000*20//100 = 800
    assert apply_coupon(cart, "TODAYCPN") == 800