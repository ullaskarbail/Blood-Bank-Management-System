CREATE DATABASE IF NOT EXISTS blood_bank;
USE blood_bank;

CREATE TABLE IF NOT EXISTS donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    blood_type VARCHAR(10) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(100) NOT NULL,
    last_donated DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blood_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blood_type VARCHAR(10) UNIQUE NOT NULL,
    units INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blood_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    blood_type VARCHAR(10) NOT NULL,
    units_required INT NOT NULL,
    hospital VARCHAR(100) NOT NULL,
    hospital_id INT,
    urgency VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS inventory_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    blood_type VARCHAR(10) NOT NULL,
    change_amount INT NOT NULL,
    units_after INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Seed Data
INSERT INTO admin (username, password) VALUES ('admin', 'scrypt:32768:8:1$Yx2q8q...$d9d20c54...'); -- Placeholder, replaced via script or python if empty, but we can do simple plain for demo or werkzeug hashed. We'll use simple plain or known hash. Let's use a known hash for 'admin123'
-- Hash for 'admin123' using pbkdf2:sha256: pbkdf2:sha256:600000$c92oO0Nl9GvV7l8D$4258c7344f6f874ab0a7cb54c7d2cbb5774a9f9c735c0a340b171c778e38d726
INSERT INTO admin (username, password) VALUES ('superadmin', 'scrypt:32768:8:1$gyfQWZkbDnO1QD8M$680382331fb054c1d0fa29f7e4cd9086c720757de9dc6ea45a0672ca74c5cea86dbb12b677257bea57188b43dbe343a00317bc636e71787818f430e2bcf3b013');

INSERT INTO blood_inventory (blood_type, units) VALUES
('A+', 10), ('A-', 5), ('B+', 15), ('B-', 2),
('O+', 20), ('O-', 3), ('AB+', 8), ('AB-', 1);

INSERT INTO hospitals (name, address, phone, email, city) VALUES 
('City General Hospital', '123 Main St', '555-0101', 'contact@citygeneral.com', 'New York'), 
('Mercy Medical Center', '456 Elm St', '555-0202', 'info@mercymedical.org', 'New York');
