import sqlite3
import datetime
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = CURRENT_DIR / "schema.sql"
DB_PATH = CURRENT_DIR / "jobs.db"

VALID_STATUSES = ['wishlist', 'applied', 'interview', 'offer', 'rejected']

class IdNotFoundError(Exception):
    pass

class WrongStatusError(Exception):
    pass

def get_conn(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # filas accesibles por nombre
    return conn

def init_db(conn):
    """Inicializa la base de datos creando la tabla jobs si no existe."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

def add_job(conn, company, position, url=None, status='wishlist', applied_at=None, notes=None):
    query = "INSERT INTO jobs (company, position, url, status, applied_at, notes) VALUES (?, ?, ?, ?, ?, ?)"
    params = (company, position, url, status, applied_at, notes)

    with conn:
        return conn.execute(query, params).lastrowid

def list_jobs(conn, status=None):
    query = "SELECT * FROM jobs"
    params = ()

    if status is not None:
        query += " WHERE status = ?"
        params = (status,)

    with conn:
        return conn.execute(query, params).fetchall()

def get_job(conn, job_id):
    query = "SELECT * FROM jobs WHERE id = ?"
    params = (job_id,)
    with conn:
        row = conn.execute(query, params).fetchone()
        if row is not None:
            return row
        else:
            raise IdNotFoundError(f"No se encontró candidatura con id {job_id}")

def delete_job(conn, job_id):
    query = "DELETE FROM jobs WHERE id = ?"
    params = (job_id,)
    with conn:
        cursor = conn.execute(query, params)
        if cursor.rowcount == 0:
            raise IdNotFoundError(f"No se encontró candidatura con id {job_id}")

def update_job(conn, job_id, status):
    if status not in VALID_STATUSES:
        raise WrongStatusError(f"Estado [{status}] inválido. Estados válidos: {VALID_STATUSES}")
    
    hoy = str(datetime.date.today())
    query = """UPDATE jobs
                SET status = ?,
                    applied_at = CASE
                        WHEN ? = 'applied' THEN COALESCE(applied_at, ?)
                        ELSE applied_at
                    END
                WHERE id = ?"""
    params = (status, status, hoy, job_id)

    with conn:
        cursor = conn.execute(query, params)
        if cursor.rowcount == 0:
            raise IdNotFoundError(f"No se encontró candidatura con id {job_id}")
