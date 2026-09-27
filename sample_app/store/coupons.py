"""Discount coupons."""
import datetime
import logging

logger = logging.getLogger(__name__)

COUPONS = {}

# Supported rule names and their corresponding predicates.
# A rule receives a Cart and returns True when the coupon may be applied.
_RULES = {
    "always": lambda cart: True,
}


def add_coupon(code, percent, expires, rule="always"):
    """Register a discount coupon.

    Args:
        code:    Unique coupon code string.
        percent: Discount percentage, must be between 1 and 100 inclusive.
        expires: datetime.date on which the coupon expires (inclusive).
        rule:    Named rule string controlling when the coupon applies.
                 Must be a key in the supported rules table.

    Raises:
        ValueError: If percent is outside 1-100 or rule is unknown.
    """
    if not (1 <= percent <= 100):
        raise ValueError(f"percent must be between 1 and 100, got {percent}")
    if rule not in _RULES:
        raise ValueError(f"unknown rule {rule!r}; valid rules: {list(_RULES)}")
    COUPONS[code] = {"percent": percent, "expires": expires, "rule": rule}


def is_valid(code, today=None):
    """Return True if the coupon exists and has not yet expired.

    Expiry is inclusive: a coupon expiring today is still valid.

    Args:
        code:  Coupon code string.
        today: Optional datetime.date to use as today (for testing).

    Returns:
        bool
    """
    today = today or datetime.date.today()
    coupon = COUPONS.get(code)
    if coupon is None:
        return False
    return coupon["expires"] >= today


def rule_allows(code, cart):
    """Return True if the named rule for this coupon allows it to apply.

    Args:
        code: Coupon code string (must already exist in COUPONS).
        cart: Cart instance to evaluate against.

    Returns:
        bool
    """
    rule_name = COUPONS[code]["rule"]
    return _RULES[rule_name](cart)


def apply_coupon(cart, code, today=None):
    """Return the cart subtotal in cents after applying the coupon discount.

    If the coupon is invalid, expired, or its rule does not allow it, the
    unmodified subtotal is returned.

    Args:
        cart:   Cart instance.
        code:   Coupon code string.
        today:  Optional datetime.date to use as today (for testing).

    Returns:
        Total in integer cents.
    """
    try:
        if is_valid(code, today) and rule_allows(code, cart):
            percent = COUPONS[code]["percent"]
            return cart.subtotal_cents() - cart.subtotal_cents() * percent // 100
        return cart.subtotal_cents()
    except Exception as e:
        logger.error("coupon error applying %r: %s", code, e)
        return cart.subtotal_cents()