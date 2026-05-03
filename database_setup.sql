-- ============================================================
--  database_setup.sql
--  Run this once in your MySQL client to set up the DB.
--  Command:  mysql -u root -p < database_setup.sql
-- ============================================================

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS signup_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE signup_db;

-- 2. Create the users table
CREATE TABLE IF NOT EXISTS users (
  id         INT          NOT NULL AUTO_INCREMENT,
  phone      VARCHAR(20)  NOT NULL,
  username   VARCHAR(60)  NOT NULL UNIQUE,
  email      VARCHAR(120) NOT NULL UNIQUE,
  password   VARCHAR(255) NOT NULL,          -- store a hashed password in production!
  created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Optional: verify
SELECT 'Database and table created successfully!' AS status;
