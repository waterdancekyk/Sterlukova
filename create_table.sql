CREATE TABLE request_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    request_id INT,
    product_name VARCHAR(255),
    quantity INT NOT NULL,
    price DECIMAL(10,2),
    production_date DATE,
    FOREIGN KEY (request_id) REFERENCES requests(request_id) ON DELETE CASCADE
);

CREATE TABLE managers (
    manager_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    position VARCHAR(100),
    department VARCHAR(100)
);

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
    sales_locations TEXT,
    discount_rate DECIMAL(5,2) DEFAULT 0.00,
    currency ENUM('RUB') DEFAULT 'RUB'
);

CREATE TABLE rating_history (
    change_id INT PRIMARY KEY AUTO_INCREMENT,
    partner_id INT,
    manager_id INT,
    previous_rating INT,
    new_rating INT,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (partner_id) REFERENCES partners(partner_id) ON DELETE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES managers(manager_id)
);

CREATE TABLE requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    partner_id INT,
    manager_id INT,
    status ENUM('created', 'approved', 'canceled', 'in_production', 'completed') DEFAULT 'created',
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prepayment_received BOOLEAN DEFAULT FALSE,
    prepayment_deadline DATE,
    delivery_method ENUM('delivery', 'pickup'),
    final_payment_received BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (partner_id) REFERENCES partners(partner_id) ON DELETE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES managers(manager_id)
);

CREATE TABLE sales_history (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    partner_id INT,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (partner_id) REFERENCES partners(partner_id) ON DELETE CASCADE
);
