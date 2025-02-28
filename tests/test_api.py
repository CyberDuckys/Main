def test_homepage(client):
    """Test of de homepage bereikbaar is."""
    response = client.get("/")
    assert response.status_code == 200

def test_api_response(client):
    """Test of de API een geldige JSON-response geeft."""
    response = client.get("/api/co2-data")
    assert response.status_code == 200
    assert response.is_json
    assert "totaal_co2" in response.json
    assert "totaal_km" in response.json
    assert "urgent_co2" in response.json
    assert "urgent_km" in response.json