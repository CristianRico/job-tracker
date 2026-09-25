-- Active: 1790243086598@@127.0.0.1@3306
CREATE TABLE candiaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa TEXT NOT NULL,
    puesto TEXT NOT NULL,
    url TEXT,
    estado TEXT DEFAULT 'wishlist' check(estado IN ('wishlist', 'applied', 'interview', 'offer', 'rejected')),
    fecha_candidatura TEXT,
    notas TEXT,
    fecha_añadida TEXT DEFAULT (date('now'))  -- formato YYYY-MM-DD
);

INSERT INTO candiaturas (empresa, puesto, url, estado, fecha_candidatura, notas) VALUES
    -- Caso 1: Solo obligatorios (aplica DEFAULTs: wishlist y fecha actual)
    ('Mercadona Tech', 'Backend Developer', NULL, 'wishlist', NULL, NULL),
    ('Glovo', 'Junior Python Dev', 'https://glovoapp.com/careers/123', 'wishlist', NULL, 'Contactar por LinkedIn con el reclutador'),
    ('Cabify', 'Data Engineer', 'https://cabify.careers/456', 'applied', '2026-09-20', 'CV enviado por la web'),
    ('Stripe', 'Software Engineer', 'https://stripe.com/jobs/789', 'interview', '2026-09-10', 'Primera llamada superada, prueba técnica el viernes'),
    ('Adevinta', 'Python Engineer', NULL, 'offer', '2026-08-15', 'Oferta: 38k brutos anuales'),
    ('Amazon', 'Support Engineer', 'https://amazon.jobs/001', 'rejected', '2026-08-01', 'Descarte automático por ATS');