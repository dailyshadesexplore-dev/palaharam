-- ============================================================
-- Palaharam — query scratchpad for the LIVE database
--
-- Live DB file:  palaharam_BE/dbConfig/Palaharam.db
-- (the palaharam.db in this folder is an old scratch copy)
--
-- Run the whole file:
--   cd palaharam_BE
--   sqlite3 dbConfig/Palaharam.db ".read sqlite/scripts.sql"
--
-- Or run queries one at a time in an interactive shell:
--   sqlite3 dbConfig/Palaharam.db
--
-- NOTE: tables are created automatically by SQLAlchemy
-- (db/models.py) when the API starts. Don't CREATE/ALTER
-- tables here — change models.py instead.
-- ============================================================

PRAGMA foreign_keys = ON;

-- Nicer output when run via .read or the shell
.headers on
.mode column

-- ------------------------------------------------------------
-- Guest orders (frontend checkouts land in this table)
-- ------------------------------------------------------------
-- SELECT id, firstName, lastName, deliveryMode, Payment_Mode,
--        totalAmount, created_at
-- FROM guests
-- ORDER BY created_at DESC;

-- -- Cart contents (JSON string) of the most recent guest order
-- SELECT id, orderDetails
-- FROM guests
-- ORDER BY created_at DESC
-- LIMIT 1;

-- ------------------------------------------------------------
-- Registered users
-- ------------------------------------------------------------
-- SELECT id, firstName, lastName, email, mobileNumber,
--        state, zipCode, created_at
-- FROM users;

-- ------------------------------------------------------------
-- Orders joined with the user who placed them
-- ------------------------------------------------------------
-- SELECT
--     o.id AS order_id,
--     o.delivery_mode,
--     o.order_details,
--     o.total_amount,
--     o.order_date,
--     u.firstName,
--     u.lastName,
--     u.email
-- FROM orders o
-- JOIN users u ON o.userId = u.id
-- ORDER BY o.order_date DESC;

-- Same report, limited to today's orders
-- SELECT
--     o.id AS order_id,
--     o.delivery_mode,
--     o.order_details,
--     o.total_amount,
--     o.order_date,
--     u.firstName,
--     u.lastName,
--     u.email
-- FROM orders o
-- JOIN users u ON o.userId = u.id
-- WHERE DATE(o.order_date) = DATE('now')
-- ORDER BY o.order_date DESC;

CREATE TABLE Menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT,
    image_url TEXT
);
INSERT INTO Menu (name, description, price, category, image_url) VALUES
-- Dishes
('Masala Dosa', 'Crispy, golden rice crepe filled with spiced potato masala, served hot with chutneys and sambar. A perfect blend of crunch and flavor.', 60, 'dishes', 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Idli', 'Soft, fluffy steamed rice cakes served with coconut chutney and piping hot sambar. A light and healthy breakfast classic.', 40, 'dishes', 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Medu Vada', 'Golden, crispy lentil doughnuts with a soft, fluffy inside. Served with chutney and sambar for the ultimate savory treat.', 45, 'dishes', 'https://images.unsplash.com/photo-1624374053855-39a5a1a41402?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Uttapam', 'Thick, soft rice pancake topped with onions, tomatoes and green chilies. A hearty and flavorful South Indian favorite.', 65, 'dishes', 'https://images.unsplash.com/photo-1736239091911-2e46d86cdc2d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Pongal', 'Comforting rice and lentil dish tempered with ghee, pepper, cumin and cashews. Warm, mild and deeply satisfying.', 55, 'dishes', 'https://images.unsplash.com/photo-1630409349197-b733a524b24e?q=80&w=2141&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Sambar', 'Tangy lentil vegetable stew with tamarind, spices and drumsticks. The perfect accompaniment to any South Indian meal.', 35, 'dishes', 'https://plus.unsplash.com/premium_photo-1700673590224-d416b98993c5?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Biryani', 'Fragrant basmati rice layered with spiced vegetables, saffron and fried onions. Rich, aromatic and full of flavor.', 150, 'dishes', 'https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?q=80&w=2088&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Appam', 'Soft, bowl-shaped fermented rice pancake with crispy edges, paired with mildly spiced coconut vegetable stew.', 80, 'dishes', 'https://plus.unsplash.com/premium_photo-1695297516748-70b4932c06d7?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

-- Beverages
('Filter Coffee', 'Strong, aromatic South Indian coffee brewed in a traditional filter and served frothy in a steel tumbler.', 25, 'beverages', 'https://images.unsplash.com/photo-1567411544047-e0cc53fe5940?q=80&w=2073&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Masala Chai', 'Classic Indian tea brewed with milk, ginger, cardamom and warming spices. Comfort in a cup.', 20, 'beverages', 'https://images.unsplash.com/photo-1646294567230-b56cb0cd1f5b?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Buttermilk', 'Refreshing spiced buttermilk with curry leaves, ginger and green chili. The perfect cooling drink.', 20, 'beverages', 'https://images.unsplash.com/photo-1630409346699-79481a79db52?q=80&w=2097&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Fresh Lime Soda', 'Zesty lime juice with soda, served sweet, salted or mixed. A fizzy, refreshing thirst quencher.', 30, 'beverages', 'https://images.unsplash.com/photo-1613478223460-f448a4de829d?q=80&w=1674&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Mango Lassi', 'Thick, creamy yogurt smoothie blended with sweet mango pulp. Rich, cool and irresistible.', 50, 'beverages', 'https://images.unsplash.com/photo-1708782343412-787fade27b60?q=80&w=1480&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),

('Tender Coconut Water', 'Naturally sweet and hydrating water served fresh from a tender coconut.', 40, 'beverages', 'https://images.unsplash.com/photo-1625535927032-dd38fdf54f84?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');


SELECT * FROM Menu;

-- DROP TABLE IF EXISTS Menu;