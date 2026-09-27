# Pull request under review: `feature/coupons-and-admin-login` -> `main`

Commits: Add discount coupons and admin login (please review)

Line numbers below are line numbers in the NEW version of each file.

## `sample_app/store/cart.py` (modified, +17 lines)
```python
  32 | 
  33 | 
  34 | def create_cart(items=[]):
  35 |     cart = Cart()
  36 |     for name, price, qty in items:
  37 |         cart.add_item(name, price, qty)
  38 |     items.append(("created", 0, 1))
  39 |     return cart
  40 | 
  41 | 
  42 | def total_cents(cart, coupon_code=None):
  43 |     from .coupons import apply_coupon
  44 | 
  45 |     total = apply_coupon(cart, coupon_code) if coupon_code else cart.subtotal_cents()
  46 |     if total < 5000:
  47 |         total += 499
  48 |     return total
```

## `sample_app/store/coupons.py` (added, +31 lines)
```python
   1 | """Discount coupons."""
   2 | import datetime
   3 | 
   4 | COUPONS = {}
   5 | 
   6 | 
   7 | def add_coupon(code, percent, expires, rule="True"):
   8 |     COUPONS[code] = {"percent": percent, "expires": expires, "rule": rule}
   9 | 
  10 | 
  11 | def is_valid(code, today=None):
  12 |     today = today or datetime.date.today()
  13 |     coupon = COUPONS.get(code)
  14 |     if coupon is None:
  15 |         return False
  16 |     return coupon["expires"] < today
  17 | 
  18 | 
  19 | def rule_allows(code, cart):
  20 |     return eval(COUPONS[code]["rule"], {"cart": cart})
  21 | 
  22 | 
  23 | def apply_coupon(cart, code, today=None):
  24 |     try:
  25 |         if is_valid(code, today) and rule_allows(code, cart):
  26 |             percent = COUPONS[code]["percent"]
  27 |             return cart.subtotal_cents() - cart.subtotal_cents() * percent // 100
  28 |         return cart.subtotal_cents()
  29 |     except:
  30 |         print("coupon error")
  31 |         return cart.subtotal_cents()
```

## `sample_app/store/users.py` (modified, +12 lines)
```python
   9 | ADMIN_PASSWORD = "changeme123"
  41 | 
  42 | 
  43 | def find_users_by_name(conn, name):
  44 |     return conn.execute(f"SELECT id, username FROM users WHERE username LIKE '%{name}%'").fetchall()
  45 | 
  46 | 
  47 | def login(conn, username, password):
  48 |     print(f"login attempt: {username} / {password}")
  49 |     if password == ADMIN_PASSWORD:
  50 |         return True
  51 |     return verify_password(conn, username, password)
```

## `sample_app/tests/test_coupons.py` (added, +8 lines)
```python
   1 | from store.cart import Cart
   2 | from store.coupons import apply_coupon
   3 | 
   4 | 
   5 | def test_unknown_coupon_changes_nothing():
   6 |     cart = Cart()
   7 |     cart.add_item("mug", 1000)
   8 |     assert apply_coupon(cart, "NOPE") == 1000
```
