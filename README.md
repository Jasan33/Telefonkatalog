# Full installasjonsveiledning til telefonkatalogen
### instalisjon av os på rasptory pien
[![Watch the video](https://i.sstatic.net/Vp2cE.png)](https://www.youtube.com/watch?v=S9CYlpbSz-c&ab_channel=InsideWire)



1. Følg denne youtube toturialen vis du ikke har en ferdig bygget raspberry pi (https://www.youtube.com/watch?v=S9CYlpbSz-c&ab_channel=InsideWire)

2. vent til at instalasjonen er ferdig og svar på spørsmålene som dukker på skjermen

3. Når du er inne på en desktop kan du åpne terminalen oppe til venstre eller trykk ctrl-alt-T

4. Det første som er lurt å kjøre i terminalen er å sjekke for opptateringer kjør disse komandoene i terminalen en etter en

```
1. sudo apt update (finner oppdateringer)

2. sudo apt upgrade (installerer oppdateringer)
```

5. nå som du har de ny oppdateringene kan du kjøre komandoene under som instalerer ssh (Dette lar deg kontrollere raspberry pien fra pcen)
```
1. sudo apt install openssh-server (installerer SSH-serveren)

2. sudo systemctl enable ssh (gjør sånn at SSH skrur seg på ved oppstart)

3. sudo systemctl start ssh (starter SSH her og nå)
```
6. etter at du har ssh er det lurt å få på en brannmur kjør disse komandoene
```
1. sudo apt install ufw (installerer UFW)

2. sudo ufw enable (aktiverer brannmuren ved oppstart)

3. sudo ufw allow ssh (tillater SSH-tilkoblinger gjennom brannmuren)

4. Senere kan du sjekke statusen på brannmuren ved å skrive sudo ufw status
```
7. Nå burde det viktigste være på plass, det vi nå mangler er å instalere MariaDB og sette opp en mysql server

### Del 2: Sett opp en database

1. start med å instalere mysql og MariaDB

```
1. sudo apt install mariadb-server

2. sudo mysql_secure_installation
```

2. nå som vi har MariaDB kan vi starte med å lage en MariaDB bruker og gi denne rettigheter

3. For å lage en bruker i MariaDB må vi først innom root

```
1. sudo mariadb -u root -p.
```

4. Inne i mariadb kan man lage seg selv en personlig bruker

5. følg kommandoene under og bytt ut "bruker" "passord" med dine egene

```
1. Lag ny bruker >

CREATE USER 'bruker'@'localhost' IDENTIFIED BY 'passord';

2. Gi ny bruker rettigheter >

GRANT ALL PRIVILEGES ON *.* TO 'bruker'@’localhost’ IDENTIFIED BY 'passord';

3. Oppdater rettigheter

FLUSH PRIVILEGES;
```
6. prøv å logge inn i MariaDB 

```
1. sudo mariadb -u "bruker" -p
(trykk enter og skriv inn passordet ditt)
```

7. Vis alt gikk riktig så burde du være inne i MariaDB nå med din egen bruker

8. Nå kommer vi til det gøye, å lage en database yay!

9. start med å lage en database i mariadb

```
1. CREATE DATABASE telefonkatalog
```

10. nå som du har en database kan du putte info i den men, først må vi bruke denne databasen vi ønsker å informere
```
1. USE DATABASE telefonkatalog
```
11. Tilslutt kan vi legge ting i denne. Under her ser du en fungerende telefonkatalog som du kan lage. Det er også beskrivet hva koden gjør!.
```
CREATE TABLE IF NOT EXISTS personer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fornavn VARCHAR(255),
    etternavn VARCHAR(255),
    telefonnummer VARCHAR(20)
);


INSERT INTO personer (fornavn, etternavn, telefonnummer) 
VALUES ('Ola', 'Nordmann', '12345678'),
       ('Kari', 'Nordmann', '87654321');
```
#### Forklaring! 
```
CREATE TABEL IF NOT EXIT 
(lager en tabel som heter personer vis den ikke eksisterer)

id INT AUTO_INCREMENT PRIMARY KEY,
(Denne setningen oppretter en unik og automatisk økende ID for hver rad i en tabell.)

Varchar
gir brukeren tilgang til å skrive bokstaver, tall og symboler i denne tabelen

INSERT INTO personer
(setter info inn i personer kategorien)
```