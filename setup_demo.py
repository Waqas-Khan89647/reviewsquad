"""One-time setup for the ReviewSquad demo. Run:  python setup_demo.py

It creates a git repository with two branches:
  main                               the shop's existing, reviewed code
  feature/coupons-and-admin-login    a teammate's pull request waiting for review
                                     (it contains problems for ReviewSquad to find)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = "feature/coupons-and-admin-login"

PR_FILES = {
    'sample_app/store/coupons.py': '"""Discount coupons."""\nimport datetime\n\nCOUPONS = {}\n\n\ndef add_coupon(code, percent, expires, rule="True"):\n    COUPONS[code] = {"percent": percent, "expires": expires, "rule": rule}\n\n\ndef is_valid(code, today=None):\n    today = today or datetime.date.today()\n    coupon = COUPONS.get(code)\n    if coupon is None:\n        return False\n    return coupon["expires"] < today\n\n\ndef rule_allows(code, cart):\n    return eval(COUPONS[code]["rule"], {"cart": cart})\n\n\ndef apply_coupon(cart, code, today=None):\n    try:\n        if is_valid(code, today) and rule_allows(code, cart):\n            percent = COUPONS[code]["percent"]\n            return cart.subtotal_cents() - cart.subtotal_cents() * percent // 100\n        return cart.subtotal_cents()\n    except:\n        print("coupon error")\n        return cart.subtotal_cents()\n',
    'sample_app/store/cart.py': '"""Shopping cart. All money is stored as integer cents."""\nfrom dataclasses import dataclass, field\nfrom typing import List\n\n\n@dataclass\nclass Item:\n    """One line in the cart."""\n\n    name: str\n    unit_price_cents: int\n    quantity: int = 1\n\n\n@dataclass\nclass Cart:\n    """A customer\'s shopping cart."""\n\n    items: List[Item] = field(default_factory=list)\n\n    def add_item(self, name, unit_price_cents, quantity=1):\n        """Add an item; quantity must be at least 1."""\n        if quantity < 1:\n            raise ValueError("quantity must be at least 1")\n        if unit_price_cents < 0:\n            raise ValueError("price cannot be negative")\n        self.items.append(Item(name, unit_price_cents, quantity))\n\n    def subtotal_cents(self):\n        """Sum of price x quantity for all items."""\n        return sum(i.unit_price_cents * i.quantity for i in self.items)\n\n\ndef create_cart(items=[]):\n    cart = Cart()\n    for name, price, qty in items:\n        cart.add_item(name, price, qty)\n    items.append(("created", 0, 1))\n    return cart\n\n\ndef total_cents(cart, coupon_code=None):\n    from .coupons import apply_coupon\n\n    total = apply_coupon(cart, coupon_code) if coupon_code else cart.subtotal_cents()\n    if total < 5000:\n        total += 499\n    return total\n',
    'sample_app/store/users.py': '"""User accounts."""\nimport hashlib\nimport hmac\nimport logging\nimport os\n\nlogger = logging.getLogger(__name__)\nHASH_ITERATIONS = 100_000\nADMIN_PASSWORD = "changeme123"\n\n\ndef hash_password(password, salt=None):\n    """Return \'salt$hash\' for a password using PBKDF2."""\n    salt = salt or os.urandom(16).hex()\n    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), HASH_ITERATIONS)\n    return f"{salt}${digest.hex()}"\n\n\ndef create_user(conn, username, password, is_admin=False):\n    """Create a user and return its id."""\n    cur = conn.execute(\n        "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",\n        (username, hash_password(password), int(is_admin)),\n    )\n    logger.info("created user %s", username)\n    return cur.lastrowid\n\n\ndef get_user(conn, user_id):\n    """Return the user row with this id, or None."""\n    return conn.execute("SELECT id, username, is_admin FROM users WHERE id = ?", (user_id,)).fetchone()\n\n\ndef verify_password(conn, username, password):\n    """Return True if the username/password pair is correct."""\n    row = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()\n    if row is None:\n        return False\n    salt, _ = row["password_hash"].split("$", 1)\n    return hmac.compare_digest(hash_password(password, salt), row["password_hash"])\n\n\ndef find_users_by_name(conn, name):\n    return conn.execute(f"SELECT id, username FROM users WHERE username LIKE \'%{name}%\'").fetchall()\n\n\ndef login(conn, username, password):\n    print(f"login attempt: {username} / {password}")\n    if password == ADMIN_PASSWORD:\n        return True\n    return verify_password(conn, username, password)\n',
    'sample_app/tests/test_coupons.py': 'from store.cart import Cart\nfrom store.coupons import apply_coupon\n\n\ndef test_unknown_coupon_changes_nothing():\n    cart = Cart()\n    cart.add_item("mug", 1000)\n    assert apply_coupon(cart, "NOPE") == 1000\n',
}


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check)


def main():
    try:
        git("--version")
    except FileNotFoundError:
        sys.exit("Git is not installed. Install it from https://git-scm.com and reopen IBM Bob.")
    if (ROOT / ".git").exists() and git("rev-parse", "--verify", BRANCH, check=False).returncode == 0:
        print("Already set up. You are ready to review.")
        return
    if not (ROOT / ".git").exists():
        git("init")
    git("checkout", "-B", "main")
    if not git("config", "user.email", check=False).stdout.strip():
        git("config", "user.email", "demo@reviewsquad.local")
        git("config", "user.name", "ReviewSquad Demo")
    git("add", "-A")
    git("commit", "-m", "CornerShop store app + ReviewSquad tool")
    git("checkout", "-b", BRANCH)
    for rel, text in PR_FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    git("add", "-A")
    git("-c", "user.name=Sam (teammate)", "-c", "user.email=sam@example.com",
        "commit", "-m", "Add discount coupons and admin login (please review)")
    git("tag", "-f", "pr-submitted")
    print("Done! Two branches created:")
    print("  main")
    print(f"  {BRANCH}   <- the pull request to review (you are on this branch now)")
    print("Next: python -m reviewsquad prepare")


if __name__ == "__main__":
    main()
