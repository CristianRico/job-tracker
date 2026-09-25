CREATE TABLE IF NOT EXISTS candidaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa TEXT NOT NULL,
    puesto TEXT NOT NULL,
    url TEXT,
    estado TEXT DEFAULT 'wishlist' check(estado IN ('wishlist', 'applied', 'interview', 'offer', 'rejected')),
    fecha_candidatura TEXT,
    notas TEXT,
    fecha_añadida TEXT DEFAULT (date('now'))  -- formato YYYY-MM-DD
);