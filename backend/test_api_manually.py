import requests
import json

"""
Detta skript hjälper dig att manuellt testa ditt API utan att behöva använda Postman eller liknande verktyg.
Kör detta skript när din Flask-server är igång.
"""

BASE_URL = "http://127.0.0.1:5000"
token = None


def print_response(response):
    """Skriver ut API-svar på ett läsbart sätt"""
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"Body: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Body: {response.text}")
    print("-" * 80)


def register_user():
    """Registrera en ny användare"""
    data = {
        "förnamn": "Test",
        "efternamn": "Användarsson",
        "email": "test_user@example.com",
        "lösenord": "TestPassword123",
        "telefon": "070-1234567"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print("\n=== REGISTRERA ANVÄNDARE ===")
    print_response(response)


def login():
    """Logga in och få JWT-token"""
    global token

    data = {
        "email": "test_user@example.com",
        "lösenord": "TestPassword123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print("\n=== LOGGA IN ===")
    print_response(response)

    if response.status_code == 200:
        token = response.json().get("token")
        print(f"Token sparad: {token[:20]}...")


def get_user_profile():
    """Hämta användarens profil (kräver autentisering)"""
    if not token:
        print("Ingen token tillgänglig. Logga in först.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/profile", headers=headers)

    print("\n=== ANVÄNDARPROFIL ===")
    print_response(response)


def create_team():
    """Skapa ett lag (kräver admin eller tränare roll)"""
    if not token:
        print("Ingen token tillgänglig. Logga in först.")
        return

    data = {
        "namn": "Testlaget",
        "beskrivning": "Ett lag skapat via API-testskriptet"
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/lag/", json=data, headers=headers)

    print("\n=== SKAPA LAG ===")
    print_response(response)


def get_all_teams():
    """Hämta alla lag"""
    response = requests.get(f"{BASE_URL}/lag/")

    print("\n=== ALLA LAG ===")
    print_response(response)


if __name__ == "__main__":
    print("API-testskript för projekt-sfc")
    print("=" * 80)
    print("Detta skript kommer att testa olika API-endpoints.")
    print("Se till att Flask-servern körs på http://127.0.0.1:5000")

    try:
        # Test API connectivity
        requests.get(f"{BASE_URL}/")
    except requests.exceptions.ConnectionError:
        print("Kunde inte ansluta till API:et. Se till att servern är igång.")
        exit(1)

    # Kör testerna
    register_user()
    login()
    get_user_profile()
    create_team()
    get_all_teams()

    print("\nTesterna är klara!")