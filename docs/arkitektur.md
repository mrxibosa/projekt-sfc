# 🏗 Arkitektur och Skalbarhet – Projekt SFC

## 1. Systemarkitektur

**Backend & API:**
- Backend med API-first-design (initialt Flask, senare Django eller FastAPI).
- REST API (eller GraphQL) byggs från början för framtida flexibilitet.
- Tydliga endpoints: användare, lag, träningar, gästbok med flera.

**Frontend:**
- Webbgränssnitt med HTML/CSS/JavaScript (framtida mobilapp med React Native eller Flutter).

**Multi-tenancy:**
- Design med stöd för flera föreningar redan från början.
- Central entitet: **Förening (`club_id`)** kopplas till användare, lag, träningar och övrig data.

---

## 2. Datamodell (fokus på multi-tenancy)

- Alla tabeller innehåller en kolumn med **`club_id`**, kopplad till respektive förening.
- Möjlighet att lägga till nya föreningar utan att ändra i koden.

---

## 3. Säkerhet och Dataisolering 🔐

- Säker autentisering med hashade lösenord (bcrypt/scrypt/argon2).
- Dataseparation: Varje förenings data isoleras med tydliga åtkomstregler.
- GDPR och hantering av personuppgifter planeras från start.

---

## 4. Monetär strategi & Licensmodell 💳

- **Freemium:** Grundfunktioner kostnadsfria, extra funktioner mot betalning.
- **Licens per förening:** Månads- eller årsavgift per förening.

---

## 5. Roadmap för Framtida Expansion 🚧

| Version | Fokusområde                          | Funktioner (exempel)                                   |
|---------|--------------------------------------|--------------------------------------------------------|
| MVP (v1)| Grundfunktionalitet för Solväders FC | Inloggning, träningsschema, gästbok                    |
| v2      | Förbättringar och fler funktioner    | Närvaro, meddelanden, grundläggande statistik          |
| v3      | Multi-tenancy (fler föreningar)      | Möjlighet att lägga till flera föreningar              |
| v4      | Mobilapp & Monetarisering            | Mobilapp, betalningsfunktioner, licenshantering        |

---

## 6. Identifierade Risker och Möjligheter 🚦

| Typ         | Beskrivning                               | Åtgärd                                           |
|-------------|-------------------------------------------|--------------------------------------------------|
| 🔴 **Risk** | Säkerhetsintrång (Sportadmin-exemplet)    | Säkerhetsstrategi, regelbundna tester, kryptering|
| 🔴 **Risk** | Dålig prestanda vid framtida expansion    | Databasoptimering och normalisering från början  |
| 🟢 **Möjlighet** | Enkel expansion till andra föreningar    | Multi-tenancy-design från början                 |
| 🟢 **Möjlighet** | Snabbare marknadsintrång via API         | API-first-strategi, flexibel integration         |
