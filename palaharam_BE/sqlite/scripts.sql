-- Enable foreign key enforcement
PRAGMA foreign_keys = ON;

-- CREATE TABLE guests(id INTEGER PRIMARY KEY, 
-- deliveryMode TEXT, 
-- firstName TEXT, 
-- lastName TEXT, 
-- address VARCHAR, 
-- mobileNumber INTEGER UNIQUE, 
-- email TEXT, 
-- state TEXT, 
-- zipCode TEXT, 
-- orderDeatails VARCHAR, 
-- created_at DATETIME DEFAULT CURRENT_TIMESTAMP );

-- INSERT INTO guests (id,deliveryMode, firstName, lastName, address, mobileNumber, email, state, zipCode, orderDeatails) VALUES 
-- (1,'Pickup', 'John', 'Doe', '123 Main St', 1234567890, 'anus@123', 'TS', '500072', '{uppama:2, pongal:1}')


-- CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, 
-- firstName TEXT, 
-- lastName TEXT, 
-- address VARCHAR, 
-- mobileNumber INTEGER UNIQUE, 
-- email TEXT UNIQUE, 
-- password TEXT,
-- state TEXT, 
-- zipCode TEXT, 
-- created_at DATETIME DEFAULT CURRENT_TIMESTAMP );

-- INSERT INTO users (firstName, lastName, address, mobileNumber, email, password, state, zipCode) VALUES 
-- ('John', 'Doe', '123 Main St', 1234567890, 'john@123', 'password@123', 'TS', '500072');

-- INSERT INTO users (firstName, lastName, address, mobileNumber, email, password, state, zipCode) VALUES 
-- ('John', 'Doe', '123 Main St', 12345890, 'john@gmail.com', 'password@123', 'TS', '500072');

CREATE TABLE orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
userId INTEGER,
deliveryMode TEXT, 
orderDeatails VARCHAR, 
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (userId) REFERENCES users(id)
);

-- INSERT INTO orders (userId, deliveryMode, orderDeatails) VALUES 
-- (1, 'delivery', '{uppama:2, pongal:1}');
-- INSERT INTO orders (userId, deliveryMode, orderDeatails) VALUES 
-- (2, 'pickup', '{uppama:2, pongal:1}');
SELECT * FROM orders;

SELECT 
    o.id AS order_id,
    o.deliveryMode,
    o.orderDeatails,
    o.created_at AS order_time,
    u.firstName,
    u.lastName,
    u.email,
    u.mobileNumber,
    u.address,
    u.state,
    u.zipCode
FROM orders o
JOIN users u ON o.userId = u.id
WHERE DATE(o.created_at) = DATE('now')
ORDER BY o.created_at DESC;
