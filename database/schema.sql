-- 1️⃣ Skapa databasen (Om den inte redan finns)
CREATE DATABASE solvaders_fc;
\c solvaders_fc;

-- 2️⃣ Skapa tabeller

-- Föreningar (Clubs)
CREATE TABLE Förening (
    club_id SERIAL PRIMARY KEY,
    namn VARCHAR(255) NOT NULL,
    stad VARCHAR(255) NOT NULL
);

-- Sporter (Stöd för flera sporter)
CREATE TABLE Sport (
    sport_id SERIAL PRIMARY KEY,
    namn VARCHAR(255) NOT NULL UNIQUE
);

-- Roller (Separerad från AnvändareFörening för flexibilitet)
CREATE TABLE Roll (
    roll_id SERIAL PRIMARY KEY,
    namn VARCHAR(50) NOT NULL UNIQUE
);

-- Lag (Teams), kopplat till Förening och Sport
CREATE TABLE Lag (
    lag_id SERIAL PRIMARY KEY,
    namn VARCHAR(255) NOT NULL,
    åldersgrupp VARCHAR(50),
    club_id INT NOT NULL,
    sport_id INT NOT NULL,
    FOREIGN KEY (club_id) REFERENCES Förening(club_id) ON DELETE CASCADE,
    FOREIGN KEY (sport_id) REFERENCES Sport(sport_id) ON DELETE CASCADE
);

-- Användare (Users) - Lagrar endast generella användaruppgifter
CREATE TABLE Användare (
    user_id SERIAL PRIMARY KEY,
    namn VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    lösenord_hash TEXT NOT NULL -- Lagrar hashade lösenord
);

-- AnvändareFörening (Kopplar användare till föreningar och roller)
CREATE TABLE AnvändareFörening (
    user_id INT,
    club_id INT,
    roll_id INT NOT NULL,
    PRIMARY KEY (user_id, club_id),
    FOREIGN KEY (user_id) REFERENCES Användare(user_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES Förening(club_id) ON DELETE CASCADE,
    FOREIGN KEY (roll_id) REFERENCES Roll(roll_id) ON DELETE CASCADE
);

-- Träningspass (Training Sessions)
CREATE TABLE Träning (
    training_id SERIAL PRIMARY KEY,
    datum_tid TIMESTAMP NOT NULL,
    plats VARCHAR(255) NOT NULL,
    lag_id INT NOT NULL,
    FOREIGN KEY (lag_id) REFERENCES Lag(lag_id) ON DELETE CASCADE
);

-- Gästbok (Message Board)
CREATE TABLE GästbokInlägg (
    inlägg_id SERIAL PRIMARY KEY,
    innehåll TEXT NOT NULL,
    skapad_datum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    club_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Användare(user_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES Förening(club_id) ON DELETE CASCADE
);
