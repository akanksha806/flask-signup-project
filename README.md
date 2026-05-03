# ✦ Flask Glassmorphism Sign-Up App

A full-stack registration form with a premium glassmorphism UI, Flask backend, and MySQL storage.

---

## Project Structure

```
flask_signup/
├── app.py                  ← Flask app (routes, validation, DB)
├── requirements.txt        ← Python dependencies
├── database_setup.sql      ← SQL to create DB & table
├── templates/
│   └── index.html          ← Jinja2 template (form UI)
└── static/
    ├── css/
    │   └── style.css       ← Glassmorphism styles
    └── js/
        └── main.js         ← Validation & AJAX submit
```

---

## ⚡ Quick Start (step-by-step)

### 1 · Install Python dependencies

```bash
pip install -r requirements.txt
```

> Requires Python 3.8+.

---

### 2 · Set up MySQL

Make sure MySQL is running, then:

```bash
mysql -u root -p < database_setup.sql
```

This creates the `signup_db` database and the `users` table.

---

### 3 · Configure database credentials

Open **`app.py`** and update the `DB_CONFIG` block:

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "your_actual_password",   # ← edit this
    "database": "signup_db",
    ...
}
```

---

### 4 · Run the app

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

---

## 🗄️ Database table schema

| Column     | Type         | Notes                        |
|------------|--------------|------------------------------|
| id         | INT (PK, AI) | Auto-increment primary key   |
| phone      | VARCHAR(20)  | User's phone number          |
| username   | VARCHAR(60)  | Unique username              |
| email      | VARCHAR(120) | Unique email address         |
| password   | VARCHAR(255) | Plain text (hash in prod!)   |
| created_at | TIMESTAMP    | Auto-set on insert           |

---

## 🔒 Production notes

- **Hash passwords** using `werkzeug.security.generate_password_hash` before storing.
- Set `debug=False` in `app.run()`.
- Use environment variables for DB credentials (e.g. `python-dotenv`).
- Add CSRF protection (`Flask-WTF`).

---

## 🎨 UI Features

- Deep purple/blue gradient background with animated glowing orbs
- Glassmorphism card — frosted glass effect via `backdrop-filter: blur()`
- Gloss reflection strip across the top of the card
- Subtle 3-D tilt effect on mouse move
- Staggered field entrance animations
- Gold/warm gradient "Sign Up" button with shine sweep on hover
- Real-time inline validation + accessible error messages
- Password show/hide toggle
- Loading spinner during form submission
- Success / error feedback without page reload (fetch API)
- Fully responsive down to 320 px

---

## Dependencies

| Library   | Purpose             |
|-----------|---------------------|
| Flask     | Web framework       |
| PyMySQL   | MySQL connector     |
