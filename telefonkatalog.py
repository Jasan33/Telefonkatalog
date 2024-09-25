import sqlite3  # Importerer biblioteket SQLite3

conn = sqlite3.connect('telefonkatalog.db') # kobler til en SQLite database med funksjonen connect(). Hvis filen 'telefonkatalog.db' ikke finnes, lages den automatisk

cursor = conn.cursor()  # Lager et objekt som lar oss bruke SQL på databasen

# Opprett en tabell hvis den ikke allerede eksisterer. Den heter 'personer' og har kolonnene 'fornavn', 'etternavn' og 'telefonnummer'. Hvis tabellen finnes fra før skjer ingenting.
cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                fornavn TEXT,
                etternavn TEXT,
                telefonnummer TEXT
            )''')

conn.commit()  # Lagrer endringene til databasen. Denne må kalles etter alle endringer i databasen.

def visAllePersoner():
    cursor.execute("SELECT * FROM personer")
    resultater = cursor.fetchall()
    if not resultater:
        print("Det er ingen registrerte personer i katalogen")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()
    else:
        print("*****************************************"
              "*****************************************")
        for personer in resultater:
            print("* Fornavn: {:15s} Etternavn: {:15s} Telfonnummer:{:8s}"
                  .format(personer[0], personer[1], personer[2]))
        print("*****************************************"
              "*****************************************")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()

# Funksjon som legger til en ny person i databasen
def legg_til_person_i_db(fornavn, etternavn, telefonnummer):
    cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (?, ?, ?)",
              (fornavn, etternavn, telefonnummer))
    conn.commit()


# Funksjon som sletter en person fra databasen basert på fornavn, etternavn og telefonnummer
def slett_person_fra_db(fornavn, etternavn, telefonnummer):
    cursor.execute("DELETE FROM personer WHERE fornavn=? AND etternavn=? AND telefonnummer=?",
              (fornavn, etternavn, telefonnummer))
    conn.commit()


def printMeny():
    print("------------------- Telefonkatalog -------------------")
    print("| 1. Legg til ny person                              |")
    print("| 2. Søk opp person eller telefonnummer              |")
    print("| 3. Vis alle personer                               |")
    print("| 4. Avslutt                                         |")
    print("------------------------------------------------------")
    menyvalg = input("Skriv inn tall for å velge fra menyen: ")
    utfoerMenyvalg(menyvalg)


def utfoerMenyvalg(valgtTall):
    if valgtTall == "1":
        registrerPerson()
    elif valgtTall == "2":
        sokPerson()
        printMeny()
    elif valgtTall == "3":
        visAllePersoner()
    elif valgtTall == "4":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if (bekreftelse == "J" or bekreftelse == "j"):
            conn.close()
            exit()
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-4: ")
        utfoerMenyvalg(nyttForsoek)


def registrerPerson():
    fornavn = input("Skriv inn fornavn: ")
    etternavn = input("Skriv inn etternavn: ")
    telefonnummer = input("Skriv inn telefonnummer: ")

    legg_til_person_i_db(fornavn, etternavn, telefonnummer) # Legger til informasjonen fra input-feltene i databasen som en ny rad

    print("{0} {1} er registrert med telefonnummer {2}"
          .format(fornavn, etternavn, telefonnummer))
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()


def sokPerson():
    print("1. Søk på fornavn")
    print("2. Søk på etternavn")
    print("3. Søk på telefonnummer")
    print("4. Tilbake til hovedmeny")
    sokefelt = input("Velg ønsket søk 1-3, eller 4 for å gå tilbake: ")
    if sokefelt == "1":
        navn = input("Fornavn: ")
        finnPerson("fornavn", navn)
    elif sokefelt == "2":
        navn = input("Etternavn: ")
        finnPerson("etternavn", navn)
    elif sokefelt == "3":
        tlfnummer = input("Telefonnummer: ")
        finnPerson("telefonnummer", tlfnummer)
    elif sokefelt == "4":
        printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-4: ")
        sokPerson()


# typeSok angir om man søker på fornavn, etternavn, eller telefonnumer
def finnPerson(typeSok, sokeTekst): # Bonus: denne funksjonen kan skrives mye kortere. Se om du klarer å forbedre den.
    if typeSok == "fornavn":
        cursor.execute("SELECT * FROM personer WHERE fornavn=?", (sokeTekst,))
    elif typeSok == "etternavn":
        cursor.execute("SELECT * FROM personer WHERE etternavn=?", (sokeTekst,))
    elif typeSok == "telefonnummer":
        cursor.execute("SELECT * FROM personer WHERE telefonnummer=?", (sokeTekst,))

    resultater = cursor.fetchall()

    if not resultater:
        print("Finner ingen personer")
    else:
        for personer in resultater:
            print("{0} {1} har telefonnummer {2}"
                  .format(personer[0], personer[1], personer[2]))


printMeny()  # Starter programmet ved å skrive menyen første gang