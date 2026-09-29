CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    url TEXT,
    status TEXT DEFAULT 'wishlist' check(status IN ('wishlist', 'applied', 'interview', 'offer', 'rejected')),
    applied_at TEXT,
    notes TEXT,
    created_at TEXT DEFAULT (date('now'))  -- formato YYYY-MM-DD
);
