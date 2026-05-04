# ============================================================
#  test_app.py — Flask App ke Tests
# ============================================================

import pytest
from app import app

# ── Test client setup ─────────────────────────────────────
@pytest.fixture
def client():
    """Har test ke liye ek test client banata hai"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ══════════════════════════════════════════════════════════
#  TEST 1 — Home page khul rahi hai ya nahi
# ══════════════════════════════════════════════════════════
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    print("✅ Home page theek se khul rahi hai")


# ══════════════════════════════════════════════════════════
#  TEST 2 — Sahi data submit karna
# ══════════════════════════════════════════════════════════
def test_valid_submission(client):
    response = client.post("/submit", data={
        "phone":    "9876543210",
        "username": "testuser",
        "email":    "test@example.com",
        "password": "secret123"
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["status"] == "success"
    print("✅ Valid form submit ho raha hai")


# ══════════════════════════════════════════════════════════
#  TEST 3 — Khaali form submit karna (error aana chahiye)
# ══════════════════════════════════════════════════════════
def test_empty_form(client):
    response = client.post("/submit", data={
        "phone":    "",
        "username": "",
        "email":    "",
        "password": ""
    })
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["status"] == "error"
    print("✅ Khaali form pe error aa raha hai")


# ══════════════════════════════════════════════════════════
#  TEST 4 — Galat email format
# ══════════════════════════════════════════════════════════
def test_invalid_email(client):
    response = client.post("/submit", data={
        "phone":    "9876543210",
        "username": "testuser",
        "email":    "yeh-email-nahi-hai",   # ← galat email
        "password": "secret123"
    })
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["status"] == "error"
    print("✅ Galat email pe error aa raha hai")


# ══════════════════════════════════════════════════════════
#  TEST 5 — Chhota password (6 se kam characters)
# ══════════════════════════════════════════════════════════
def test_short_password(client):
    response = client.post("/submit", data={
        "phone":    "9876543210",
        "username": "testuser",
        "email":    "test@example.com",
        "password": "abc"              # ← sirf 3 characters
    })
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["status"] == "error"
    print("✅ Chhote password pe error aa raha hai")


# ══════════════════════════════════════════════════════════
#  TEST 6 — Chhota username (3 se kam characters)
# ══════════════════════════════════════════════════════════
def test_short_username(client):
    response = client.post("/submit", data={
        "phone":    "9876543210",
        "username": "ab",              # ← sirf 2 characters
        "email":    "test@example.com",
        "password": "secret123"
    })
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["status"] == "error"
    print("✅ Chhote username pe error aa raha hai")


# ══════════════════════════════════════════════════════════
#  TEST 7 — Phone number missing
# ══════════════════════════════════════════════════════════
def test_missing_phone(client):
    response = client.post("/submit", data={
        "phone":    "",                # ← phone nahi diya
        "username": "testuser",
        "email":    "test@example.com",
        "password": "secret123"
    })
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data["status"] == "error"
    print("✅ Phone missing pe error aa raha hai")