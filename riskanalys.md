# 🚩 Riskanalys – Projekt SFC

## A. Risker relaterade till Solväders FC (nuvarande behov)

| Risk | Sannolikhet | Påverkan | Mitigeringsstrategi |
|------|-------------|----------|---------------------|
| **Felaktiga krav**: Systemet uppfyller inte Solväders FC:s specifika behov. | Medel | Hög | Noggrann kravinsamling, kontinuerlig feedback från användare, iterativ utveckling. |
| **Låg användaradoption**: Användarna är ovilliga att använda systemet. | Medel | Hög | Användarvänligt gränssnitt, enkel onboarding, tydlig kommunikation om fördelarna. |
| **Dataintegritet**: Felaktig eller förlorad data. | Låg | Hög | Robust databasdesign, regelbunden backup, datavalidering. |
| **Säkerhetsbrister**: Obefogad åtkomst till känslig information. | Medel | Hög | Säkra kodningsmetoder, robust autentisering och auktorisering, regelbundna säkerhetsgranskningar. |

---

## B. Risker relaterade till skalbarhet (framtida expansion)

| Risk | Sannolikhet | Påverkan | Mitigeringsstrategi |
|------|-------------|----------|---------------------|
| **Skalbarhetsproblem**: Klarar ej stor mängd användare/föreningar. | Medel | Hög | Skalbar teknologi (Django, PostgreSQL), horisontell skalning, caching. |
| **Komplexitet i multi-tenancy**: Svårt hantera flera föreningar. | Medel | Medel | Noggrann datamodell, tydlig data-isolering, multi-tenant-ramverk. |
| **Dataisolering**: Risk att data blandas mellan föreningar. | Låg | Hög | Dataseparation på databas- och applikationsnivå, strikt åtkomstkontroll. |
| **Anpassning till olika föreningar**: Svårt anpassa systemet till olika behov. | Medel | Medel | Flexibel datamodell, konfigurerbara inställningar. |
| **API-kompatibilitet**: Problem vid integration med andra system. | Låg | Medel | Välutformade och dokumenterade API:er (RESTful/GraphQL). |

---

## 🚧 Hur vi hanterar riskerna:

- **Prioritera Solväders FC först**: Fokusera på kategori A (nuvarande risker) först.
- **Skalbarhet som princip**: Välj teknologier som stödjer skalbarhet.
- **Modularitet**: Bygg i moduler som kan utökas och anpassas.
- **API-first approach**: Designa API:er tidigt för enkel framtida integration.

Denna strategi ger en bra balans mellan att leverera ett effektivt system idag och förbereda för framtida tillväxt.
