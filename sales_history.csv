CREATE TABLE sales_history (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    partner_id INT,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (partner_id) REFERENCES partners(partner_id) ON DELETE CASCADE
);
