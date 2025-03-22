def test_minimal(client):
    assert client is not None
    assert isinstance(client, object)  # Eller något enkelt jämförelse
