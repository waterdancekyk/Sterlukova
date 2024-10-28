LOAD DATA INFILE '/path/to/partners.csv' 
INTO TABLE partners 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS; -- Игнорируем заголовок (если он есть)
