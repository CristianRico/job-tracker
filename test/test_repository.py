import pytest
import datetime
import repository as db

@pytest.fixture
def conn():
    conn = db.get_conn(":memory:")
    db.init_db(conn)
    yield conn
    conn.close()

@pytest.fixture
def conn_con_candidaturas(conn):
    db.add_candidatura(conn, "Acme", "Junior Python Dev")
    db.add_candidatura(conn, "Globex", "Backend Developer", estado="applied", fecha_candidatura="2026-09-20")
    db.add_candidatura(conn, "Initech", "Data Engineer", estado="applied", fecha_candidatura="2026-09-22")
    return conn

def test_add_candidatura(conn):
    row_id = db.add_candidatura(conn, "Claude", "CEO", url="http://claude.io", fecha_candidatura="2025-02-01", notas="esta es una nota")
    row = conn.execute(
        "SELECT * FROM candidaturas WHERE id = ?", [row_id]
    ).fetchone()

    assert isinstance(row_id,int)
    assert row is not None
    assert row["empresa"] == "Claude"
    assert row["puesto"] == "CEO"
    assert row["url"] == "http://claude.io"
    assert row["estado"] == "wishlist"
    assert row["fecha_candidatura"] == "2025-02-01"
    assert row["notas"] == "esta es una nota"
    assert row["fecha_añadida"] == str(datetime.date.today())

def test_list_candidaturas(conn_con_candidaturas):
    rows = db.list_candidaturas(conn_con_candidaturas)
    assert len(rows) == 3

def test_list_candidaturas_estado(conn_con_candidaturas):
    rows = db.list_candidaturas(conn_con_candidaturas, "applied")
    assert len(rows) == 2
    assert rows[0]["estado"] == "applied"
    assert rows[0]["empresa"] == "Globex" 
    assert rows[1]["empresa"] == "Initech" 

def test_list_candidaturas_vacia(conn):
    rows = db.list_candidaturas(conn)
    assert len(rows) == 0

def test_show_candidatura_wrong_id(conn_con_candidaturas):
    id = 4
    with pytest.raises(db.IdNotFoundError, match=f"No se encontró candidatura con id {id}"):
        db.show_candidatura(conn_con_candidaturas, id)

def test_show_candidatura(conn_con_candidaturas):
    candidatura_id = 1
    row = db.show_candidatura(conn_con_candidaturas, id)
    assert row is not None
    assert row["id"] == candidatura_id
    assert row["empresa"] == "Acme"
