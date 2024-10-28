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