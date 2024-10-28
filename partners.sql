CREATE TABLE partners (
    partner_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    type ENUM('retail', 'wholesale', 'online', 'corporate') NOT NULL,
    legal_address VARCHAR(255),
    inn VARCHAR(12) UNIQUE,
    director_name VARCHAR(255),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(100),
    logo BLOB,
    rating INT DEFAULT 0,
    sales_locations TEXT,  -- JSON формат для хранения мест продаж
    discount_rate DECIMAL(5,2) DEFAULT 0.00,  -- скидка, зависящая от объема продаж
    currency ENUM('RUB') DEFAULT 'RUB'
);