-- 旅遊系統 資料庫 Schema

-- 景點表 (ATTRACTION)
CREATE TABLE IF NOT EXISTS attraction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    location TEXT NOT NULL,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 餐廳表 (RESTAURANT)
CREATE TABLE IF NOT EXISTS restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    attraction_id INTEGER,
    description TEXT,
    rating REAL,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attraction_id) REFERENCES attraction (id)
);

-- 行程總表 (ITINERARY)
CREATE TABLE IF NOT EXISTS itinerary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 行程項目表 (ITINERARY_ITEM)
CREATE TABLE IF NOT EXISTS itinerary_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    itinerary_id INTEGER NOT NULL,
    item_type TEXT NOT NULL, -- 'attraction' 或 'restaurant'
    item_id INTEGER NOT NULL,
    event_time DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (itinerary_id) REFERENCES itinerary (id)
);
