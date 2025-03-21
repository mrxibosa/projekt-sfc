-- 1️⃣ Lägg in sporter
INSERT INTO Sport (namn) VALUES ('Fotboll'), ('Basket'), ('Tennis');

-- 2️⃣ Lägg in en förening
INSERT INTO Förening (namn, stad) VALUES ('Solväders FC', 'Göteborg');

-- 3️⃣ Lägg in användare
INSERT INTO Användare (namn, email, lösenord_hash) VALUES
('Alice Andersson', 'alice@example.com', 'hashed_password_1'),
('Bob Bengtsson', 'bob@example.com', 'hashed_password_2'),
('Charlie Carlsson', 'charlie@example.com', 'hashed_password_3');

-- 4️⃣ Lägg in roller
INSERT INTO Roll (namn) VALUES ('spelare'), ('tränare'), ('admin');

-- 5️⃣ Koppla användare till föreningen med roller
INSERT INTO AnvändareFörening (user_id, club_id, roll_id) VALUES
(1, 1, 1),  -- Alice är spelare i Solväders FC
(2, 1, 2),  -- Bob är tränare i Solväders FC
(3, 1, 3);  -- Charlie är admin i Solväders FC

-- 6️⃣ Lägg in ett lag i föreningen kopplat till en sport
INSERT INTO Lag (namn, åldersgrupp, club_id, sport_id) VALUES
('Solväders P18', 'U18', 1, 1);

-- 7️⃣ Lägg in ett träningspass för laget
INSERT INTO Träning (datum_tid, plats, lag_id) VALUES
('2025-04-01 18:00:00', 'Solväders IP', 1);

-- 8️⃣ Lägg in ett gästboksinlägg
INSERT INTO GästbokInlägg (innehåll, user_id, club_id) VALUES
('Välkommen till Solväders FCs nya hemsida!', 3, 1);
