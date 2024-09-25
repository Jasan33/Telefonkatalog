-- en tabell for personer
CREATE TABLE IF NOT EXISTS personer (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Legg til en primærnøkkel
    fornavn VARCHAR(255),
    etternavn VARCHAR(255),
    telefonnummer VARCHAR(20)
);

-- setter inn noen eksempel navn
INSERT INTO personer (fornavn, etternavn, telefonnummer) 
VALUES ('Ola', 'Nordmann', '12345678'),
       ('Kari', 'Nordmann', '87654321');