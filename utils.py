# =============================================================
#  utils.py  —  Simple Python Helper Functions
#  Yeh functions puri application mein use hote hain
# =============================================================

import re


# ── Function 1: Phone number validate karna ───────────────────
def is_valid_phone(phone):
    """
    Phone number valid hai ya nahi check karta hai.
    Sirf digits allowed hain, minimum 7 aur maximum 15.
    Example: "9876543210" → True
             "abc"        → False
    """
    phone = phone.strip()
    return bool(re.match(r"^\+?[\d\s\-]{7,15}$", phone))


# ── Function 2: Email validate karna ─────────────────────────
def is_valid_email(email):
    """
    Email address valid format mein hai ya nahi.
    Example: "user@gmail.com" → True
             "user@"          → False
    """
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email.strip()))


# ── Function 3: Username clean karna ─────────────────────────
def format_username(username):
    """
    Username ko lowercase aur trimmed karta hai.
    Spaces ko underscore se replace karta hai.
    Example: "  Hello World  " → "hello_world"
    """
    return username.strip().lower().replace(" ", "_")


# ── Function 4: Password strength check karna ────────────────
def check_password_strength(password):
    """
    Password kitna strong hai check karta hai.
    Returns: "weak", "medium", ya "strong"

    weak   → 6 se kam characters
    medium → 6+ characters, sirf letters ya sirf numbers
    strong → 8+ characters, letters + numbers dono hain
    """
    if len(password) < 6:
        return "weak"
    has_letters = bool(re.search(r"[a-zA-Z]", password))
    has_digits  = bool(re.search(r"\d", password))
    if len(password) >= 8 and has_letters and has_digits:
        return "strong"
    return "medium"
