# =============================================================
#  test_app.py  —  Unit Tests (4 alag alag tarike)
#
#  Tarika 1: Simple assert tests       (seedha sach/jhooth check)
#  Tarika 2: pytest.mark.parametrize  (ek test, kai inputs)
#  Tarika 3: Exception testing         (galti aane ki umeed)
#  Tarika 4: Flask integration tests   (puri app test)
# =============================================================

import pytest
from utils import is_valid_phone, is_valid_email, format_username, check_password_strength
from app import app


# ══════════════════════════════════════════════════════════════
#  TARIKA 1 — Simple Assert Tests
#  Seedha function call karo aur result check karo
#  Sabse basic aur beginner-friendly tarika
# ══════════════════════════════════════════════════════════════

class TestSimpleAssert:
    """Tarika 1: Seedhe assert se test"""

    # Phone number tests
    def test_valid_phone_number(self):
        assert is_valid_phone("9876543210") == True

    def test_invalid_phone_letters(self):
        assert is_valid_phone("abcdefgh") == False

    def test_empty_phone(self):
        assert is_valid_phone("") == False

    def test_phone_with_plus(self):
        assert is_valid_phone("+91 9876543210") == True

    # Email tests
    def test_valid_email(self):
        assert is_valid_email("user@gmail.com") == True

    def test_invalid_email_no_at(self):
        assert is_valid_email("usergmail.com") == False

    def test_invalid_email_empty(self):
        assert is_valid_email("") == False

    # Username format tests
    def test_username_lowercase(self):
        assert format_username("HELLO") == "hello"

    def test_username_spaces_to_underscore(self):
        assert format_username("hello world") == "hello_world"

    def test_username_strips_spaces(self):
        assert format_username("  akanksha  ") == "akanksha"

    # Password strength tests
    def test_weak_password(self):
        assert check_password_strength("abc") == "weak"

    def test_medium_password(self):
        assert check_password_strength("abcdefgh") == "medium"

    def test_strong_password(self):
        assert check_password_strength("hello123") == "strong"


# ══════════════════════════════════════════════════════════════
#  TARIKA 2 — Parametrize Tests
#  Ek test function, kai alag inputs — code repeat nahi hota
#  Jab bahut saare cases test karne ho tab use karo
# ══════════════════════════════════════════════════════════════

class TestParametrize:
    """Tarika 2: Parametrize se kai inputs ek saath test"""

    # Phone: valid cases
    @pytest.mark.parametrize("phone", [
        "9876543210",
        "+91 9876543210",
        "1234567",
        "+1-800-555-0199",
    ])
    def test_valid_phones(self, phone):
        assert is_valid_phone(phone) == True

    # Phone: invalid cases
    @pytest.mark.parametrize("phone", [
        "",
        "abc",
        "12",        # bahut chhota
        "@@@@",
    ])
    def test_invalid_phones(self, phone):
        assert is_valid_phone(phone) == False

    # Email: valid cases
    @pytest.mark.parametrize("email", [
        "user@gmail.com",
        "test@yahoo.in",
        "hello@company.org",
        "a@b.co",
    ])
    def test_valid_emails(self, email):
        assert is_valid_email(email) == True

    # Email: invalid cases
    @pytest.mark.parametrize("email", [
        "",
        "nogmail",
        "no@domain",
        "@missing.com",
    ])
    def test_invalid_emails(self, email):
        assert is_valid_email(email) == False

    # Password strength: input → expected output
    @pytest.mark.parametrize("password,expected", [
        ("abc",       "weak"),
        ("12345",     "weak"),
        ("abcdefgh",  "medium"),
        ("12345678",  "medium"),
        ("hello123",  "strong"),
        ("Pass1234",  "strong"),
    ])
    def test_password_strength_levels(self, password, expected):
        assert check_password_strength(password) == expected

    # Username formatting
    @pytest.mark.parametrize("input_name,expected", [
        ("HELLO",         "hello"),
        ("Hello World",   "hello_world"),
        ("  akanksha  ",  "akanksha"),
        ("Test USER",     "test_user"),
    ])
    def test_username_formatting(self, input_name, expected):
        assert format_username(input_name) == expected


# ══════════════════════════════════════════════════════════════
#  TARIKA 3 — Edge Case & Type Tests
#  Unusual inputs: None, numbers, special characters
#  Yeh dekhta hai ki function crash toh nahi karta
# ══════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Tarika 3: Edge cases aur unusual inputs"""

    def test_email_with_spaces_only(self):
        assert is_valid_email("   ") == False

    def test_email_multiple_at_signs(self):
        assert is_valid_email("a@@b.com") == False

    def test_phone_only_spaces(self):
        assert is_valid_phone("   ") == False

    def test_username_already_clean(self):
        assert format_username("akanksha") == "akanksha"

    def test_username_all_caps(self):
        result = format_username("AKANKSHA GUPTA")
        assert result == "akanksha_gupta"

    def test_password_exactly_6_chars(self):
        # exactly 6 characters, sirf letters → medium
        assert check_password_strength("abcdef") == "medium"

    def test_password_exactly_8_with_digit(self):
        # exactly 8, letters + digit → strong
        assert check_password_strength("abcdef1g") == "strong"

    def test_password_empty(self):
        assert check_password_strength("") == "weak"

    def test_phone_with_hyphens(self):
        assert is_valid_phone("98-765-43210") == True


# ══════════════════════════════════════════════════════════════
#  TARIKA 4 — Flask Integration Tests
#  Puri Flask app ko test karta hai (routes + validation)
#  Real HTTP requests jaisi testing
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Flask test client — har test ke liye fresh client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestFlaskRoutes:
    """Tarika 4: Flask routes ki integration testing"""

    def test_home_page_loads(self, client):
        """/ route → 200 OK aana chahiye"""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_page_has_form(self, client):
        """Home page mein form hona chahiye"""
        response = client.get("/")
        assert b"form" in response.data.lower()

    def test_valid_form_submission(self, client):
        """/submit route sahi data pe success deta hai"""
        response = client.post("/submit", data={
            "phone":    "9876543210",
            "username": "testuser99",
            "email":    "test99@example.com",
            "password": "secret123"
        })
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["status"] == "success"

    def test_empty_form_returns_error(self, client):
        """Khaali form pe 400 error aana chahiye"""
        response = client.post("/submit", data={
            "phone": "", "username": "", "email": "", "password": ""
        })
        assert response.status_code == 400
        assert response.get_json()["status"] == "error"

    def test_invalid_email_returns_error(self, client):
        """Galat email pe 400 error"""
        response = client.post("/submit", data={
            "phone": "9876543210", "username": "testuser",
            "email": "yeh-email-nahi", "password": "secret123"
        })
        assert response.status_code == 400

    def test_short_password_returns_error(self, client):
        """6 se kam password pe 400 error"""
        response = client.post("/submit", data={
            "phone": "9876543210", "username": "testuser",
            "email": "test@example.com", "password": "abc"
        })
        assert response.status_code == 400

    def test_short_username_returns_error(self, client):
        """2 character username pe 400 error"""
        response = client.post("/submit", data={
            "phone": "9876543210", "username": "ab",
            "email": "test@example.com", "password": "secret123"
        })
        assert response.status_code == 400

    def test_missing_phone_returns_error(self, client):
        """Phone number missing pe 400 error"""
        response = client.post("/submit", data={
            "phone": "", "username": "testuser",
            "email": "test@example.com", "password": "secret123"
        })
        assert response.status_code == 400

    def test_invalid_route_returns_404(self, client):
        """Galat URL pe 404 aana chahiye"""
        response = client.get("/koi-bhi-galat-url")
        assert response.status_code == 404