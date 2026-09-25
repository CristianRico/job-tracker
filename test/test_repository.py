import pytest
import datetime
import repository as db

@pytest.fixture
def conn():
    conn = db.get_conn(":memory:")
    db.init_db(conn)
    yield conn
    conn.close()

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