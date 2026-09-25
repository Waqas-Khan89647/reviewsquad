"""Discount coupons."""
import datetime

COUPONS = {}


def add_coupon(code, percent, expires, rule="True"):
    COUPONS[code] = {"percent": percent, "expires": expires, "rule": rule}


def is_valid(code, today=None):
    today = today or datetime.date.today()
    coupon = COUPONS.get(code)
    if coupon is None:
        return False
    return coupon["expires"] < today


def rule_allows(code, cart):
    return eval(COUPONS[code]["rule"], {"cart": cart})


def apply_coupon(cart, code, today=None):
    try:
        if is_valid(code, today) and rule_allows(code, cart):
            percent = COUPONS[code]["percent"]
            return cart.subtotal_cents() - cart.subtotal_cents() * percent // 100
        return cart.subtotal_cents()
    except:
        print("coupon error")
        return cart.subtotal_cents()
