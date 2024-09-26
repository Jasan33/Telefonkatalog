import mysql.connector  # Importerer MySQL-connector

# Koble til MySQL-databasen
conn = mysql.connector.connect(
    host="10.2.4.41",
    user="Jasan",
    password="abcd1234",
    database="telefonkatalog"
)

cursor = conn.cursor()

# Opprett en tabell hvis den ikke allerede eksisterer
cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fornavn VARCHAR(255),
                etternavn VARCHAR(255),
                telefonnummer VARCHAR(20)
            )''')

conn.commit()  # Lagrer endringene til databasen

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
        for person in resultater:
            print("* Fornavn: {:15s} Etternavn: {:15s} Telefonnummer: {:8s}"
                  .format(person[1], person[2], person[3]))
        print("*****************************************"
              "*****************************************")
        input("Trykk en tast for å gå tilbake til menyen")
        printMeny()

# Funksjon som legger til en ny person i databasen
def legg_til_person_i_db(fornavn, etternavn, telefonnummer):
    cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)",
              (fornavn, etternavn, telefonnummer))
    conn.commit()


# Funksjon som sletter en person fra databasen basert på fornavn, etternavn og telefonnummer
def slett_person_fra_db(fornavn, etternavn, telefonnummer):
    cursor.execute("DELETE FROM personer WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
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

    legg_til_person_i_db(fornavn, etternavn, telefonnummer)  # Legger til informasjonen i databasen

    print("{0} {1} er registrert med telefonnummer {2}".format(fornavn, etternavn, telefonnummer))
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


def finnPerson(typeSok, sokeTekst):
    # Sjekker om typeSok er en gyldig kolonne for å unngå SQL-injection
    if typeSok not in ["fornavn", "etternavn", "telefonnummer"]:
        print("Ugyldig søkekategori.")
        return
    
    query = f"SELECT * FROM personer WHERE {typeSok} = %s"
    cursor.execute(query, (sokeTekst,))
    resultater = cursor.fetchall()

    if not resultater:
        print("Finner ingen personer")
    else:
        for person in resultater:
            print("{0} {1} har telefonnummer {2}".format(person[1], person[2], person[3]))