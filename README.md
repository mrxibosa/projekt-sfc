# ⚽ Projekt SFC – Vision & Planering

## 🎯 1. Projektmål
Projekt SFC är en säker och användarvänlig webbplattform för fotbollsföreningen Solväders FC. Målet är att skapa en stabil, krypterad och framtidssäker lösning där spelare, tränare och administratörer kan hantera lagets aktiviteter.

---

## 👥 2. Användartyper
| Typ        | Roll / Funktion |
|------------|----------------|
| **Spelare** | Logga in, se träningsschema, skriva i gästbok |
| **Tränare** | Skapa schema, hantera grupp, skicka meddelanden |
| **Admin**   | Hantera användare, lag och innehåll |
| **Gäst**    | Läsa nyheter, skriva i gästbok |

---

## 🛠 3. Teknikval
| Del       | Verktyg |
|-----------|--------|
| Backend  | Python (Flask, ev. Django senare) |
| Frontend | HTML, CSS, JavaScript (React eller Vue i framtiden) |
| Databas  | MySQL (normaliserad) |
| Säkerhet | Kryptering (bcrypt/scrypt), sessionshantering |
| Versionshantering | Git + GitHub |
| UI-design | Enkel prototyp, senare mobilanpassning |

---

## 🏗 4. Funktioner

### 🔐 4.1 Inloggningssida
- Registrering med rollval
- Inloggning (hashad verifiering)
- Eventuell mejlbekräftelse (framtid)

### 🏠 4.2 Start- & infosida
- Nyheter från klubben
- Kontaktinfo
- Välkomsttext och bild
- "Senaste från lagen"

### 🏟️ 4.3 Lagspecifika funktioner
- Se träningsschema
- Närvaroanmälan
- Gästbok (med namn, koppling till lag)
- Enkla spelarprofiler

### ⚙️ 4.4 Admin- & Tränarfunktioner
- Skapa/redigera träningar
- Skicka gruppmeddelanden
- Hantera användare
- Se statistik / närvaro

### 🚀 4.5 Framtid & Skalning
- Bildgalleri
- Matchresultat & statistik
- Intern chatt eller notiser
- Mobilapp (React Native / Flutter)
- Betalfunktioner (medlemsavgift, shop)

---

## 📦 5. Version 1 – MVP
> **Fokus i första versionen:**
- Inloggning & registrering
- Startsida med info
- Gästbok
- Träningsschema (visning)
- GitHub-repo med versionshantering
- Enkel men ren UI med HTML/CSS

---

## 🚀 6. Roadmap
- ✅ Skapa GitHub-repo
- ⏳ Planera databasstruktur
- ⏳ Bygga backend (Flask + SQL)
- ⏳ Grundläggande frontend (HTML/CSS)
- ⏳ Testa och förbättra UI
- ⏳ Säkerhet och kryptering
- ⏳ Skala upp till en fullständig plattform

---

## 📌 Scope – Version 1 (MVP)
Det här ingår i version 1 av projektet:
- Stöd för rollerna: spelare, tränare, admin
- Inloggning och registrering
- Gästbok (med namn och meddelande)
- Träningsschema per lag (visning)
- Grundläggande webbgränssnitt med HTML/CSS
- Allt versionhanteras med GitHub

Funktioner som inte ingår i version 1:
- Bildgalleri
- Intern chatt
- Betalning
- Statistik
- Mobilapp

## 🏗 7. GitHub-struktur
/projekt-sfc ├── backend/ # Flask + SQL ├── frontend/ # HTML, CSS, JavaScript ├── database/ # MySQL-skript och ER-diagram ├── docs/ # Dokumentation & kravspecifikation ├── tests/ # Testkod och säkerhetstester ├── README.md # Dokumentation (du läser den nu!)


