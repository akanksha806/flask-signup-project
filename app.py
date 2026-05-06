# =============================================================
#  app.py  —  Flask App (Users + Education)
# =============================================================

import re
from flask import Flask, render_template, request, jsonify

try:
    import pymysql
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

app = Flask(__name__)

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "akanksha@123",
    "database": "signup_db",
    "charset":  "utf8mb4",
}

def get_db():
    print("👉 Trying DB connection...")
    if not DB_AVAILABLE:
        print("❌ pymysql not installed")
        return None
    try:
        cfg = dict(DB_CONFIG)
        cfg["cursorclass"] = pymysql.cursors.DictCursor
        conn = pymysql.connect(**cfg)
        print("✅ DB CONNECTED SUCCESSFULLY")
        return conn
    except Exception as e:
        print(f"❌ DB ERROR: {e}")
        return None

def validate_user(data):
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

def validate_education(data):
    errors = []
    if not data.get("username"):       errors.append("Username required.")
    if not data.get("college_name"):   errors.append("College name required.")
    if not data.get("degree"):         errors.append("Degree required.")
    if not data.get("year"):           errors.append("Year required.")
    if not data.get("city"):           errors.append("City required.")
    return errors

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = {k: request.form.get(k, "").strip()
            for k in ["phone","username","email","password"]}
    errors = validate_user(data)
    if errors:
        return jsonify({"status":"error","messages":errors}), 400
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (phone,username,email,password) VALUES (%s,%s,%s,%s)",
                    (data["phone"],data["username"],data["email"],data["password"])
                )
            conn.commit()
        except pymysql.err.IntegrityError:
            return jsonify({"status":"error","messages":["Username/email already exists."]}), 409
        except Exception as e:
            return jsonify({"status":"error","messages":[str(e)]}), 500
        finally:
            conn.close()
    else:
        print(f"[DEMO] User: {data['username']}")
    return jsonify({"status":"success","message":f"Welcome {data['username']}! Account created."})

@app.route("/education")
def education():
    users = []
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users ORDER BY username")
                users = [r["username"] for r in cur.fetchall()]
        except: pass
        finally: conn.close()
    return render_template("education.html", users=users)

@app.route("/submit-education", methods=["POST"])
def submit_education():
    data = {k: request.form.get(k,"").strip()
            for k in ["username","college_name","degree","year","city"]}
    errors = validate_education(data)
    if errors:
        return jsonify({"status":"error","messages":errors}), 400
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE username=%s", (data["username"],))
                if not cur.fetchone():
                    return jsonify({"status":"error","messages":["Username registered nahi hai."]}), 400
                cur.execute(
                    "INSERT INTO education (username,college_name,degree,year,city) VALUES (%s,%s,%s,%s,%s)",
                    (data["username"],data["college_name"],data["degree"],data["year"],data["city"])
                )
            conn.commit()
        except Exception as e:
            return jsonify({"status":"error","messages":[str(e)]}), 500
        finally:
            conn.close()
    else:
        print(f"[DEMO] Education: {data['username']}")
    return jsonify({"status":"success","message":f"{data['username']} ki education details save ho gayi!"})

@app.route("/combined")
def combined():
    rows, df_html, df_stats = [], "", {}
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT u.id, u.username, u.email, u.phone,
                           e.college_name, e.degree, e.year, e.city
                    FROM users u
                    INNER JOIN education e ON u.username = e.username
                    ORDER BY u.username
                """)
                rows = cur.fetchall()
        except Exception as e:
            print(f"[JOIN] {e}")
        finally:
            conn.close()

    if PANDAS_AVAILABLE and rows:
        df = pd.DataFrame(rows)
        df_html  = df.to_html(classes="dataframe", index=False, border=0)
        df_stats = {
            "total_rows":    len(df),
            "total_columns": len(df.columns),
            "columns":       list(df.columns),
            "cities":        df["city"].unique().tolist(),
            "degrees":       df["degree"].unique().tolist(),
        }
        df.to_csv("combined_data.csv", index=False)
        print("\n[DataFrame]\n", df.to_string(), f"\nShape: {df.shape}")

    return render_template("combined.html", rows=rows, df_html=df_html, df_stats=df_stats)

if __name__ == "__main__":
    app.run(debug=True)