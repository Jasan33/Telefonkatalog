import mysql.connector  # Importerer MySQL-connector
import webbrowser # Importerer WebBrowser

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

telefonkatalog = []  # listeformat ["fornavn", "etternavn", "telefonnummer"]

def printMeny():
    print("----------------------Telefonkatalog----------------------")
    print("|  1. Legg til ny person                                 |")
    print("|  2. Søk opp person eller telefonnummer                 |")
    print("|  3. Vis alle personer                                  |")
    print("|  4. Slett en person                                    |")
    print("|  5. følg meg 😊😊                                      |")
    print("|  6. Avslutt                                            |")
    print("----------------------------------------------------------")
    menyvalg = input("skriv inn tall for å velge fra menyen: ")
    utfoerMenyvalg(menyvalg)


def utfoerMenyvalg(valgtTall):
    if valgtTall == "1":  
        registrerPerson()
    elif valgtTall == "2":
        sokPerson()
    elif valgtTall == "3":
        visAllePersoner()
    elif valgtTall == "4":
        slett()  # Merk at jeg har endret til liten "s"
    elif valgtTall == "5":
        folg()
    elif valgtTall == "6":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if bekreftelse == "J" or bekreftelse == "j":  # sjekker for både stor og liten bokstav
            conn.close()
            exit()
    else:
        nyttforsoek = input("Ugyldig valg. Velg et tall mellom 1-4: ")
        utfoerMenyvalg(nyttforsoek)

def registrerPerson():
    fornavn = input("skriv inn fornavn: ")
    etternavn = input("skriv inn etternavn: ")
    telefonnummer = input("skriv inn telefonnummer: ")

    nyRegistrering = [fornavn, etternavn, telefonnummer]
    telefonkatalog.append(nyRegistrering)

    legg_til_person_i_db(fornavn, etternavn, telefonnummer)

    print("{0} {1} er registrert med telefonnummer {2}"
          .format(fornavn, etternavn, telefonnummer))
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()


def visAllePersoner():
    cursor.execute("SELECT * FROM personer")
    telefonkatalog = cursor.fetchall()
    if not telefonkatalog:
        print("Det er ingen registrerte personer i katalogen")
    else:
        print("************************************************************************************")
        for personer in telefonkatalog:
            # Merk at personer[0] er ID, som er et heltall (int)
            print("* ID: {:3d} Fornavn: {:15s} Etternavn: {:15s} Telefonnummer: {:8s}"
                  .format(personer[0], personer[1], personer[2], personer[3]))
        print("************************************************************************************")
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()

def sokPerson():
    if not telefonkatalog:
        print("Det er ingen registrerte personer i katalogen")
        printMeny()
    else:
        print("1. søk på fornavn")
        print("2. søk på etternavn")
        print("3. søk på telefonnummer")
        print("4. Tilbake til hovedmeny")
        sokefelt = input("velg ønsket søk 1-3, eller 4 for å gå tilbake: ")
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
            print("ugyldig valg. Velg et tall mellom 1-4: ")
            sokPerson()


# typeSok angir om man søker på fornavn, etternavn, eller telefonnummer
def finnPerson(typesok, sokeTekst):
    funnet = False
    for personer in telefonkatalog:
        if typesok == "fornavn" and personer[0] == sokeTekst:
            cursor.execute("SELECT * FROM personer WHERE fornavn=?", (sokeTekst,))
            print("{0} {1} har telefonnummer {2}"
                  .format(personer[0], personer[1], personer[2]))
            funnet = True
        elif typesok == "etternavn" and personer[1] == sokeTekst:
            cursor.execute("SELECT * FROM personer WHERE etternavn=?", (sokeTekst,))
            print("{0} {1} har telefonnummer {2}"
                  .format(personer[0], personer[1], personer[2]))
            funnet = True
        elif typesok == "telefonnummer" and personer[2] == sokeTekst:
            cursor.execute("SELECT * FROM personer WHERE telefonnummer=?", (sokeTekst,))
            print("telefonnummer {0} tilhører {1} {2}"
                  .format(personer[2], personer[0], personer[1]))
            telefonkatalog = cursor.fetchall()
            funnet = True
    if not funnet:
        print(f"Finner ingen personer med {typesok}: {sokeTekst}")
    sokPerson()

def slettPerson(typesok, sokeTekst):
    global telefonkatalog
    funnet = False
    ny_katalog = []
    for personer in telefonkatalog:
        if (typesok == "fornavn" and personer[0] == sokeTekst) or \
           (typesok == "etternavn" and personer[1] == sokeTekst) or \
           (typesok == "telefonnummer" and personer[2] == sokeTekst):
            print(f"Person {personer[0]} {personer[1]} med telefonnummer {personer[2]} er slettet.")
            slett_person_fra_db(personer[0], personer[1], personer[2])  # Slett fra databasen
            funnet = True
        else:
            ny_katalog.append(personer)
    
    if not funnet:
        print(f"Fant ingen personer med {typesok}: {sokeTekst}")
    
    telefonkatalog = ny_katalog
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()

def slett():
    if not telefonkatalog:
        print("Det er ingen registrerte personer i katalogen")
    else:
        print("1. Slett etter fornavn")
        print("2. Slett etter etternavn")
        print("3. Slett etter telefonnummer")
        print("4. Tilbake til hovedmeny")
        valg = input("Velg ønsket søkemetode 1-3, eller 4 for å gå tilbake: ")

        if valg == "1":
            navn = input("Fornavn: ")
            slettPerson("fornavn", navn)
        elif valg == "2":
            navn = input("Etternavn: ")
            slettPerson("etternavn", navn)
        elif valg == "3":
            tlfnummer = input("Telefonnummer: ")
            slettPerson("telefonnummer", tlfnummer)
        elif valg == "4":
            printMeny()
        else:
            print("Ugyldig valg. Velg et tall mellom 1-4.")
            slett()

def folg():
    webbrowser.open("http://github.com/Jasan33/")
    print("gi meg en follow! https://github.com/Jasan33")
    print("Trykk en tast for å gå tilbake til menyen")
    input()
    printMeny()
def slettPerson(typesok, sokeTekst):
    global telefonkatalog
    funnet = False
    ny_katalog = []
    for personer in telefonkatalog:
        if (typesok == "fornavn" and personer[0] == sokeTekst) or \
           (typesok == "etternavn" and personer[1] == sokeTekst) or \
           (typesok == "telefonnummer" and personer[2] == sokeTekst):
            print(f"Person {personer[0]} {personer[1]} med telefonnummer {personer[2]} er slettet.")
            funnet = True
        else:
            ny_katalog.append(personer)
    
    if not funnet:
        print(f"Fant ingen personer med {typesok}: {sokeTekst}")
    
    telefonkatalog = ny_katalog
    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()



printMeny()  # starter programmet ved å skrive menyen første gang
