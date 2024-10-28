CREATE TABLE request_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    request_id INT,
    product_name VARCHAR(255),
    quantity INT NOT NULL,
    price DECIMAL(10,2),
    production_date DATE,
    FOREIGN KEY (request_id) REFERENCES requests(request_id) ON DELETE CASCADE
);
