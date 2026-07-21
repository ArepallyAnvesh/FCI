-- ============================================================
-- Farmer Consumer Interaction (FCI) - Database Script
-- ============================================================

DROP DATABASE IF EXISTS farmer_consumer;
CREATE DATABASE farmer_consumer;
USE farmer_consumer;

-- ------------------------------------------------------------
-- Table: farmers
-- ------------------------------------------------------------
CREATE TABLE farmers (
    farmer_id     INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    mobile        VARCHAR(15)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    address       VARCHAR(255) NOT NULL,
    password      VARCHAR(100) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: consumers
-- ------------------------------------------------------------
CREATE TABLE consumers (
    consumer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    mobile        VARCHAR(15)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    address       VARCHAR(255) NOT NULL,
    password      VARCHAR(100) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: products
-- ------------------------------------------------------------
CREATE TABLE products (
    product_id    INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id     INT NOT NULL,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50)  NOT NULL,
    price         DECIMAL(10,2) NOT NULL,
    quantity      INT NOT NULL,
    description   TEXT,
    image_path    VARCHAR(255),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_farmer
        FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table: contact_messages
-- ------------------------------------------------------------
CREATE TABLE contact_messages (
    message_id    INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL,
    message       TEXT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Sample data (optional, for quick testing)
-- ------------------------------------------------------------
INSERT INTO farmers (name, mobile, email, address, password)
VALUES ('Ramesh Kumar', '9876543210', 'ramesh@example.com', 'Nalgonda, Telangana', 'ramesh123');

INSERT INTO consumers (name, mobile, email, address, password)
VALUES ('Anita Sharma', '9123456780', 'anita@example.com', 'Hyderabad, Telangana', 'anita123');

INSERT INTO products (farmer_id, product_name, category, price, quantity, description, image_path)
VALUES
(1, 'Fresh Tomatoes', 'Vegetables', 25.00, 100, 'Farm fresh, pesticide-free tomatoes harvested this week.', 'images/tomato.jpg'),
(1, 'Basmati Rice', 'Grains', 80.00, 50, 'Premium quality basmati rice, 1kg pack.', 'images/rice.jpg');
