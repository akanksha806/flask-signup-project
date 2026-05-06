-- ============================================================
--  database_update.sql
--  Education table banao + Foreign Key lagao
--  Run: mysql -u root -p signup_db < database_update.sql
-- ============================================================

USE signup_db;

-- Education table banao
CREATE TABLE IF NOT EXISTS education (
  id           INT          NOT NULL AUTO_INCREMENT,
  username     VARCHAR(60)  NOT NULL,
  college_name VARCHAR(150) NOT NULL,
  degree       VARCHAR(60)  NOT NULL,
  year         VARCHAR(20)  NOT NULL,
  city         VARCHAR(80)  NOT NULL,
  created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),

  -- Foreign Key → users.username se connect
  CONSTRAINT fk_edu_username
    FOREIGN KEY (username)
    REFERENCES users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Verify karo
SELECT 'Education table ready!' AS status;

-- ── JOIN Query (test karne ke liye) ──────────────────────────
-- SELECT u.id, u.username, u.email, u.phone,
--        e.college_name, e.degree, e.year, e.city
-- FROM users u
-- INNER JOIN education e ON u.username = e.username
-- ORDER BY u.username;
