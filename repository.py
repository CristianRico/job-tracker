import sqlite3

DB_PATH = "jobs.db"
DB_QUERY = """
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
            """
ESTADOS_VALIDOS = ['wishlist', 'applied', 'interview', 'offer', 'rejected']

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # filas accesibles por nombre
    return conn

def init_db(conn):
    """Inicializa la base de datos creando la tabla jobs si no existe."""
    with conn:
            conn.execute(DB_QUERY)
            conn.commit()

def add_candidatura(conn, empresa, puesto, url=None, estado='wishlist', fecha_candidatura=None, notas=None):
    with conn:
        cur = conn.execute(
            "INSERT INTO candidaturas (empresa, puesto, url, estado, fecha_candidatura, notas) VALUES (?, ?, ?, ?, ?, ?)",
            (empresa, puesto, url, estado, fecha_candidatura, notas),
        )
        return cur.lastrowid

def list_candidaturas(conn):
    with conn:
        return conn.execute("SELECT * FROM jobs").fetchall()