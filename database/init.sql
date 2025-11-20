CREATE DATABASE IF NOT EXISTS face_auth;
USE face_auth;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL CHECK (CHAR_LENGTH(password) >= 6)
);

ALTER TABLE users
ADD COLUMN first_name VARCHAR(255) NOT NULL,
ADD COLUMN last_name VARCHAR(255) NOT NULL,
ADD COLUMN email VARCHAR(255) UNIQUE NOT NULL;

ALTER TABLE users
ADD CONSTRAINT email_format CHECK (email LIKE '%@gmail.com');

CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(255) NOT NULL
);

DELIMITER $$

CREATE TRIGGER validate_user_before_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    -- Kiểm tra username không được để trống
    IF NEW.username IS NULL OR CHAR_LENGTH(NEW.username) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username must not be empty';
    END IF;

    -- Kiểm tra username phải có ít nhất 5 ký tự
    IF CHAR_LENGTH(NEW.username) < 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username must be at least 5 characters long';
    END IF;

    -- Kiểm tra password không được để trống
    IF NEW.password IS NULL OR CHAR_LENGTH(NEW.password) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must not be empty';
    END IF;

    -- Kiểm tra password phải có ít nhất 6 ký tự
    IF CHAR_LENGTH(NEW.password) < 6 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must be at least 6 characters long';
    END IF;
END$$

DELIMITER ;

-- Xóa user dựa trên username
DELETE FROM users
WHERE username = 'tên_user_cần_xóa';