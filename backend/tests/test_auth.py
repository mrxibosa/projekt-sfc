# tests/test_auth.py
import pytest
from flask import json


def test_login_success(client, test_user):
    """
    Testar inloggning med korrekt lösenord.
    Förväntad respons: 200 OK med ett token.
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'losenord': 'test123'
    })

    assert response.status_code == 200, f"Förväntade 200, men fick {response.status_code}"
    data = response.get_json()
    assert 'token' in data, f"Token saknas i svar: {data}"


def test_login_wrong_password(client, test_user):
    """
    Testar inloggning med fel lösenord.
    Förväntad respons: 401 Unauthorized med felmeddelande.
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'losenord': 'felLösen123'
    })

    assert response.status_code == 401, f"Förväntade 401, men fick {response.status_code}"
    data = response.get_json()
    assert 'error' in data, f"Felmeddelande saknas i svar: {data}"


def test_login_nonexistent_user(client):
    """
    Testar inloggning med en icke-existerande användare.
    Förväntad respons: 401 Unauthorized.
    """
    response = client.post('/auth/login', json={
        'email': 'nobody@example.com',
        'losenord': 'whatever123'
    })

    assert response.status_code == 401, f"Förväntade 401, men fick {response.status_code}"
    data = response.get_json()
    assert 'error' in data, f"Felmeddelande saknas i svar: {data}"


def test_login_missing_fields(client):
    """
    Testar inloggning med saknade fält.
    Förväntad respons: 400 Bad Request.
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com'
        # lösenord saknas
    })

    assert response.status_code == 400, f"Förväntade 400, men fick {response.status_code}"
    data = response.get_json()
    assert 'error' in data, f"Felmeddelande saknas i svar: {data}"