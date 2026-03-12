import os

FILE_NAME = "film.txt"

def carica_film():    
    if not os.path.exists(FILE_NAME):
        print('Errore nel collegamento')
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        film = [riga.strip() for riga in f if riga.strip()]
    return film

def salva_film(film):
   
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for titolo in film:
            f.write(titolo + "\n")

def visualizza_film(film):
    
    print("Film visti:")
    if not film:
        print(" (Nessun film nella collezione)")
    else:
        for i, titolo in enumerate(film, 1):
            print(f"  {i}. {titolo}")
    print()

def inserisci_film(film):
    
    titolo = input("Titolo del film da aggiungere: ").strip()
    if not titolo:
        print("Titolo non valido.")
        return
    if titolo.lower() in [f.lower() for f in film]:
        print("Film già presente nella collezione.")
        return
    film.append(titolo)
    print(f"'{titolo}' aggiunto con successo.")

def modifica_film(film):
    
    visualizza_film(film)
    if not film:
        return
    try:
        scelta = int(input("Numero del film da modificare: "))
        if not 1 <= scelta <= len(film):
            print("Numero non valido.\n")
            return
    except:
        print("Inserire un numero valido.\n")
        return

    vecchio = film[scelta - 1]
    nuovo = input(f"Nuovo titolo per '{vecchio}': ").strip()
    if not nuovo:
        print("Titolo non valido.")
        return
    film[scelta - 1] = nuovo
    print(f" '{vecchio}' rinominato in '{nuovo}'.")

def cancella_film(film):
    
    visualizza_film(film)
    if not film:
        return
    try:
        scelta = int(input("Numero del film da cancellare: "))
        if not 1 <= scelta <= len(film):
            print("Numero non valido.")
            return
    except:
        print("Inserire un numero valido.")
        return

    titolo = film.pop(scelta - 1)
    print(f" '{titolo}' rimosso dalla collezione.")


    
  

def menu():
    print("VIDEOTECA DIGITALE")
    print("  1. Visualizza film")
    print("  2. Aggiungi film")
    print("  3. Modifica film")
    print("  4. Cancella film")
    print("  5. Salva collezione")
    print("  0. Esci")
    return input("Scelta: ").strip()

film = carica_film()
print(f" Caricati {len(film)} film da '{FILE_NAME}'.")
run=True
while run==True:
    scelta = menu()
    if scelta == "1":
        visualizza_film(film)
    elif scelta == "2":
        inserisci_film(film)
    elif scelta == "3":
        modifica_film(film)
    elif scelta == "4":
        cancella_film(film)
    elif scelta == "0":
        print("Arrivederci!")
        salva_film(film)
        print("Collezione salvata con successo!")
        run=False
    else:
        print("Scelta non valida.")
