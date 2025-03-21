🏗 1. Arkitektur & skalbarhet

1.1. Systemarkitektur

Backend/API-first (t.ex. Flask, senare Django/FastAPI)
Frontend: Webb (HTML/CSS/JS) → mobilapp (framtiden, React Native eller Flutter)
Multi-tenancy (stöd för flera föreningar)
Central entitet: Förening (Club), som kopplas till användare, lag, träningar, osv.

1.2. Datamodell (fokus på multi-tenancy)

Alla tabeller kopplas till en förening (club_id)
Möjlighet att lägga till nya föreningar utan kodändringar

1.3. API-first

REST API (eller GraphQL) från början, för framtida flexibilitet
Klara endpoints: användare, lag, träningar, gästbok, osv.

🔐 2. Säkerhet och dataisolering
Säker autentisering med hashade lösenord (bcrypt/scrypt/argon2)
Dataseparation: varje förenings data är isolerad med tydliga åtkomstregler
GDPR och dataintegritet från början (personuppgiftshantering)

💳 3. Monetär strategi & licensmodell (framtida expansion)
Potentiell licensmodell:
Freemium (gratis basfunktioner, premiumfunktioner mot avgift)
Per förening (månads/årsavgift per förening)

🚧 4. Roadmap för framtida expansion
Version	Fokusområde	Funktioner (exempel)
MVP (v1)	Grundfunktionalitet för Solväders FC	Inloggning, träningsschema, gästbok
v2	Förbättringar & Fler funktioner	Närvaro, meddelanden, grundläggande statistik
v3	Multi-tenancy (fler föreningar)	Stöd för att lägga till flera föreningar
v4	Mobilapp & Monetarisering	Mobilapp, betalningsfunktioner, licenshantering

🚦 5. Identifierade risker och möjligheter
Typ	Beskrivning	Åtgärd
Risk	Säkerhetsintrång (Sportadmin-exemplet)	Tydlig säkerhetsstrategi, tester, kryptering
Risk	Dålig prestanda vid expansion	Databasoptimering, normalisering från början
Möjlighet	Enkel expansion till andra föreningar	Multi-tenancy-design från början
Möjlighet	Snabbare marknadsintrång via API	Bygg API tidigt, möjlighet till integration
