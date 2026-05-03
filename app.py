# =============================================================
#  app.py  —  Flask Registration App
#  Run:  python app.py
# =============================================================

import re
from flask import Flask, render_template, request, jsonify

# ── optional MySQL import ─────────────────────────────────────
try:
    import pymysql
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

app = Flask(__name__)

# ── Database configuration ────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "akanksha@123",  # ← yeh bilkul sahi likho
    "database": "signup_db",
    "charset":  "utf8mb4",
}

# ── helper: get a DB connection ───────────────────────────────
def get_db():
    if not DB_AVAILABLE:
        return None
    try:
        cfg = {k: v for k, v in DB_CONFIG.items() if k != "cursorclass"}
        cfg["cursorclass"] = pymysql.cursors.DictCursor
        return pymysql.connect(**cfg)
    except Exception as e:
        print(f"[DB] Connection failed: {e}")
        return None

# ── helper: basic validation ──────────────────────────────────
def validate(data):
    errors = []
    if not data.get("phone"):
        errors.append("Phone number is required.")
    if not data.get("username") or len(data["username"]) < 3:
        errors.append("Username must be at least 3 characters.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get("email", "")):
        errors.append("Invalid email address.")
    if not data.get("password") or len(data["password"]) < 6:
        errors.append("Password must be at least 6 characters.")
    return errors

# ── routes ────────────────────────────────────────────────────
@app.route("/")
def index():
    """Serve the registration form."""
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = {
        "phone":    request.form.get("phone",    "").strip(),
        "username": request.form.get("username", "").strip(),
        "email":    request.form.get("email",    "").strip(),
        "password": request.form.get("password", "").strip(),
    }

    errors = validate(data)
    if errors:
        return jsonify({"status": "error", "messages": errors}), 400

    conn = get_db()
    
    # Yeh line add karo — connection check ke liye
    print("DB Connection:", conn)
    
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO users (phone, username, email, password)
                       VALUES (%s, %s, %s, %s)""",
                    (data["phone"], data["username"], data["email"], data["password"]),
                )
            conn.commit()
            print("Saved to DB successfully!")  # ← yeh bhi add karo
        except Exception as e:
            print("DB ERROR:", e)  # ← error yahan dikhega
            conn.close()
            return jsonify({"status": "error", "messages": [str(e)]}), 500
        finally:
            conn.close()

    return jsonify({
        "status":  "success",
        "message": f"Welcome, {data['username']}! Your account has been created.",
    })


if __name__ == "__main__":
    app.run(debug=True)
