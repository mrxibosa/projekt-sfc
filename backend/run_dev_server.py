from app import app

"""
Detta skript startar utvecklingsservern med debugläge aktiverat.
Du kan köra den direkt genom:
python run_dev_server.py
"""

if __name__ == "__main__":
    print(f"Startar server med databas: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Besök http://127.0.0.1:5000 för att komma åt API:et")
    print(f"Tillgängliga rutter:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint} - {rule.methods} - {rule}")

    app.run(debug=True, host='0.0.0.0', port=5000)