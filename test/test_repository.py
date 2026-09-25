import pytest
import datetime
import re
import repository as db

@pytest.fixture
def conn():
    conn = db.get_conn(":memory:")
    db.init_db(conn)
    yield conn
    conn.close()

@pytest.fixture
def conn_with_jobs(conn):
    db.add_job(conn, "Acme", "Junior Python Dev")
    db.add_job(conn, "Globex", "Backend Developer", status="applied", applied_at="2026-09-20")
    db.add_job(conn, "Initech", "Data Engineer", status="applied", applied_at="2026-09-22")
    return conn

@pytest.fixture
def conn_with_job_date(conn):
    db.add_job(conn, "Acme", "Junior Python Dev", applied_at="2026-09-20")
    return conn

def test_add_job(conn):
    row_id = db.add_job(conn, "Claude", "CEO", url="http://claude.io", applied_at="2025-02-01", notes="esta es una nota")
    row = conn.execute(
        "SELECT * FROM jobs WHERE id = ?", [row_id]
    ).fetchone()

    assert isinstance(row_id,int)
    assert row is not None
    assert row["company"] == "Claude"
    assert row["position"] == "CEO"
    assert row["url"] == "http://claude.io"
    assert row["status"] == "wishlist"
    assert row["applied_at"] == "2025-02-01"
    assert row["notes"] == "esta es una nota"
    assert row["created_at"] == str(datetime.date.today())

def test_list_jobs(conn_with_jobs):
    rows = db.list_jobs(conn_with_jobs)
    assert len(rows) == 3

def test_list_jobs_by_status(conn_with_jobs):
    rows = db.list_jobs(conn_with_jobs, "applied")
    assert len(rows) == 2
    assert rows[0]["status"] == "applied"
    assert rows[0]["company"] == "Globex" 
    assert rows[1]["company"] == "Initech" 

def test_list_jobs_empty(conn):
    rows = db.list_jobs(conn)
    assert len(rows) == 0

def test_get_job_wrong_id(conn_with_jobs):
    job_id = 4
    with pytest.raises(db.IdNotFoundError, match=f"No se encontró candidatura con id {job_id}"):
        db.get_job(conn_with_jobs, job_id)

def test_get_job(conn_with_jobs):
    job_id = 1
    row = db.get_job(conn_with_jobs, job_id)
    assert row is not None
    assert row["id"] == job_id
    assert row["company"] == "Acme"

def test_delete_job(conn_with_jobs):
    job_id = 1
    db.delete_job(conn_with_jobs, job_id)
    with pytest.raises(db.IdNotFoundError, match=f"No se encontró candidatura con id {job_id}"):
        db.get_job(conn_with_jobs, job_id)

def test_delete_job_wrong_id(conn_with_jobs):
    job_id = 4
    with pytest.raises(db.IdNotFoundError, match=f"No se encontró candidatura con id {job_id}"):
        db.delete_job(conn_with_jobs, job_id)

def test_update_job(conn_with_jobs):
    job_id = 1
    status = "rejected"
    db.update_job(conn_with_jobs, job_id, status)
    row = db.get_job(conn_with_jobs, job_id)
    assert row["status"] == status

def test_update_job_wrong_status(conn_with_jobs):
    job_id = 1
    status = "wrong"
    msg = f"Estado [{status}] inválido. Estados válidos: {db.VALID_STATUSES}"
    with pytest.raises(db.WrongStatusError, match=re.escape(msg)):
        db.update_job(conn_with_jobs, job_id, status)

def test_update_job_wrong_id(conn_with_jobs):
    job_id = 4
    status = "rejected"
    with pytest.raises(db.IdNotFoundError, match=f"No se encontró candidatura con id {job_id}"):
        db.update_job(conn_with_jobs, job_id, status)

#Al pasar a applied sin fecha, se guarda la de hoy
def test_update_applied_nodate(conn_with_jobs):
    job_id = 1
    old_job = db.get_job(conn_with_jobs, job_id)

    db.update_job(conn_with_jobs, 1, "applied")

    new_job = db.get_job(conn_with_jobs, job_id)
    hoy = str(datetime.date.today())

    assert old_job["applied_at"] == None
    assert new_job["applied_at"] == hoy

#Al pasar a applied con fecha, se mantiene la fecha original
def test_update_applied_date(conn_with_job_date):
    job_id = 1
    old_job = db.get_job(conn_with_job_date, job_id)

    db.update_job(conn_with_job_date, 1, "applied")

    new_job = db.get_job(conn_with_job_date, job_id)

    assert old_job["applied_at"] == new_job["applied_at"]