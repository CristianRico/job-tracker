import sqlite3
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = CURRENT_DIR / "schema.sql"
DB_PATH = CURRENT_DIR / "jobs.db"

ESTADOS_VALIDOS = ['wishlist', 'applied', 'interview', 'offer', 'rejected']

class IdNotFoundError(Exception):
    pass

def get_conn(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # filas accesibles por nombre
    return conn

def init_db(conn):
    """Inicializa la base de datos creando la tabla candidaturas si no existe."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

def add_candidatura(conn, empresa, puesto, url=None, estado='wishlist', fecha_candidatura=None, notas=None):
    query = "INSERT INTO candidaturas (empresa, puesto, url, estado, fecha_candidatura, notas) VALUES (?, ?, ?, ?, ?, ?)"
    params = (empresa, puesto, url, estado, fecha_candidatura, notas)

    with conn:
        return conn.execute(query, params).lastrowid

def list_candidaturas(conn, estado=None):
    query = "SELECT * FROM candidaturas"
    params = ()

    if estado is not None:
        query += " WHERE estado = ?"
        params = (estado,)

    with conn:
        return conn.execute(query, params).fetchall()

def show_candidatura(conn, id):
    query = "SELECT * FROM candidaturas WHERE id = ?"
    params = (id,)
    with conn:
        row = conn.execute(query, params).fetchone()
        if row is not None:
            return row
        else:
            raise IdNotFoundError(f"No se encontró candidatura con id {id}")