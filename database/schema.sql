CREATE DATABASE IF NOT EXISTA expense_tracker;

USE expense_tracker;

CREATE TABLE IF NOT EXIST expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),
    amount DECIMAL(10, 2),
    date DATE,

)