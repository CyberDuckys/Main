def test_database_connection(db_connection):
    """Test of de databaseverbinding succesvol tot stand komt."""
    assert db_connection.is_connected()

def test_fetch_data(db_cursor):
    """Test of er gegevens kunnen worden opgehaald uit een tabel."""
    db_cursor.execute("SELECT * FROM bestellingen LIMIT 1;")
    result = db_cursor.fetchall()
    assert result is not None