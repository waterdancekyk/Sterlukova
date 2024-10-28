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