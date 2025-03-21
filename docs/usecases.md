# 📘 Use Cases – Projekt SFC

Här beskrivs de viktigaste användarinteraktionerna med systemet i version 1 (MVP). Varje use case innehåller användartyp, mål och ett kort flöde.

---

## 🎯 UC1 – Registrera konto
**Användare:** Spelare, tränare, admin  
**Mål:** Skapa ett nytt konto  
**Flöde:**  
1. Användaren öppnar registreringssidan  
2. Fyller i användarnamn, lösenord, e-post och roll  
3. Klickar på "Registrera"  
4. Kontot skapas och användaren omdirigeras till inloggningssidan

---

## 🎯 UC2 – Logga in
**Användare:** Alla  
**Mål:** Få tillgång till systemet  
**Flöde:**  
1. Användaren öppnar inloggningssidan  
2. Fyller i användarnamn och lösenord  
3. Systemet verifierar inloggningen  
4. Användaren loggas in och hamnar på sin startsida

---

## 🎯 UC3 – Visa träningsschema
**Användare:** Spelare  
**Mål:** Se sitt lags träningar  
**Flöde:**  
1. Spelaren loggar in  
2. Systemet identifierar spelarens lag  
3. Systemet visar en lista med kommande träningar

---

## 🎯 UC4 – Skapa träning
**Användare:** Tränare  
**Mål:** Lägga till ett nytt träningstillfälle  
**Flöde:**  
1. Tränaren loggar in  
2. Går till “Skapa träning”  
3. Fyller i datum, tid, plats och val av lag  
4. Träningen sparas i databasen och visas för lagets spelare

---

## 🎯 UC5 – Skriva i gästbok
**Användare:** Spelare eller gäst  
**Mål:** Skriva ett meddelande  
**Flöde:**  
1. Användaren öppnar gästboken  
2. Skriver sitt namn och meddelande  
3. Klickar på "Skicka"  
4. Meddelandet sparas och visas i listan

---

## 🎯 UC6 – Hantera användare
**Användare:** Admin  
**Mål:** Skapa, redigera eller ta bort användare  
**Flöde:**  
1. Admin loggar in  
2. Går till användarhantering  
3. Väljer åtgärd (lägg till, redigera, ta bort)  
4. Bekräftar och ändringar sparas

