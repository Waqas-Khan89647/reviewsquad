# ReviewSquad review

**Verdict: REQUEST CHANGES**  
17 findings: 10 high, 4 medium, 3 low.  
Reviewers: guidelines (3), logic (5), security (5), tests (4)

## 🔴 High

- [ ] **Expiry check is inverted: valid coupons are rejected, expired ones accepted** (`store/coupons.py:16`, logic reviewer)  
  Fix: Change the comparison from < to >= so that a coupon expiring today is still valid. Rule 2.4 states expiry dates are inclusive.
- [ ] **eval() called on coupon rule string (arbitrary code execution)** (`store/coupons.py:20`, security reviewer)  
  Fix: Replace eval() with a safe predicate system. Define an enum or a small set of named rules and look them up by key instead of evaluating arbitrary strings. Guideline 1.4.
- [ ] **Hard-coded admin password in source code** (`store/users.py:9`, security reviewer)  
  Fix: Remove ADMIN_PASSWORD from source. Load it from an environment variable: os.environ['ADMIN_PASSWORD']. Guideline 1.1.
- [ ] **SQL injection via f-string in find_users_by_name()** (`store/users.py:44`, security reviewer)  
  Fix: Use a parameterised query: conn.execute('SELECT id, username FROM users WHERE username LIKE ?', (f'%{name}%',)). Guideline 1.2.
- [ ] **Password logged in plain text via print()** (`store/users.py:48`, security reviewer)  
  Fix: Remove the print statement entirely. Never log credentials. Guideline 1.3.
- [ ] **Master-password backdoor bypasses normal authentication** (`store/users.py:49`, security reviewer)  
  Fix: Delete the 'if password == ADMIN_PASSWORD: return True' block entirely. All logins must go through verify_password(). Guideline 1.5.
- [ ] **No tests for is_valid(): the inverted expiry bug has no test coverage** (`tests/test_coupons.py:1`, tests reviewer)  
  Fix: Add tests: valid coupon (expires today), expired coupon (yesterday), future coupon. Rule 3.1.
- [ ] **No tests for apply_coupon() with a valid discount coupon** (`tests/test_coupons.py:1`, tests reviewer)  
  Fix: Add a test that adds a coupon with a known percent discount, calls apply_coupon, and asserts the correct discounted total. Rule 3.1.
- [ ] **New public functions total_cents, create_cart, find_users_by_name, login have zero tests** (`tests/test_coupons.py:1`, tests reviewer)  
  Fix: Add test files for cart and user functions covering normal, edge, and error cases for each new public function. Rule 3.1.
- [ ] **rule_allows() / eval() path is completely untested** (`tests/test_coupons.py:1`, tests reviewer)  
  Fix: Add tests for rule_allows() with a passing rule and a failing rule. Once eval is replaced with safe predicates, test each predicate type. Rule 3.1.

## 🟠 Medium

- [ ] **Mutable default argument items=[] shared across all calls** (`store/cart.py:34`, logic reviewer)  
  Fix: Change signature to create_cart(items=None) and add 'if items is None: items = []' at the top of the function. Rule 2.3.
- [ ] **create_cart() appends a sentinel to the caller's list, mutating it unexpectedly** (`store/cart.py:38`, logic reviewer)  
  Fix: Remove the items.append line entirely. It has no documented purpose and silently corrupts the caller's input list. Rule 2.3.
- [ ] **add_coupon() does not validate that percent is 1-100 or that expires is a date** (`store/coupons.py:7`, guidelines reviewer)  
  Fix: Add guard clauses: raise ValueError if percent is outside 1-100. Rule 2.1 requires input validation at the point of entry.
- [ ] **Bare except: swallows all exceptions including KeyboardInterrupt and SystemExit** (`store/coupons.py:29`, logic reviewer)  
  Fix: Replace 'except:' with 'except Exception as e:' and use logger.exception or logger.error to record the error. Rule 2.5.

## 🟡 Low

- [ ] **Magic numbers 5000 and 499 used for delivery fee threshold and fee amount** (`store/cart.py:46`, logic reviewer)  
  Fix: Extract named constants, e.g. FREE_DELIVERY_THRESHOLD_CENTS = 5000 and DELIVERY_FEE_CENTS = 499. Rule 4.2.
- [ ] **All new public functions lack docstrings (add_coupon, is_valid, rule_allows, apply_coupon, find_users_by_name, login, create_cart, total_cents)** (`store/coupons.py:7`, guidelines reviewer)  
  Fix: Add a one-line docstring to every public function explaining its purpose, parameters, and return value. Rule 4.1.
- [ ] **print() used instead of logging module in coupons.py and users.py** (`store/coupons.py:30`, guidelines reviewer)  
  Fix: Replace print() calls with logger.error() or logger.warning(). Both files already have or should have a module-level logger. Rule 4.3.
