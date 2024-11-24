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

CREATE TABLE IF NOT EXISTS passese (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Legg til en primærnøkkel
    brukernavn VARCHAR(200),
    dittpass VARCHAR(200) default NULL
);

INSERT INTO passese (brukernavn, dittpass)
VALUES ('Olam',aes_encrypt('passorda', 'key1234'));