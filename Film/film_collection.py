import csv
import json
import os

FILE_CSV = "film.csv"
FILE_JSON = "film.json"
SEPARATORE = "|"

film = [
    {
        "titolo": "La cosa",
        "anno": 1983,
        "incassi": 20100000
    }
]


def inserisci(film):
    err_nome = True
    while err_nome:
        nome = input("Inserisci il titolo del film: ").capitalize()
        if nome != "":
            print("Nome registrato")
            err_nome = False
        else:
            print("Titolo vuoto non valido")

    err_anno = True
    while err_anno:
        try:
            anno = int(input("Inserisci anno di uscita del film: "))
            if anno > 1895:
                print("Anno di uscita registrato")
                err_anno = False
            else:
                raise ValueError
        except ValueError:
            print("Anno inserito non valido")

    err_incasso = True
    while err_incasso:
        try:
            incasso = float(input("Inserisci gli incassi al botteghino di questo film: "))
            if incasso >= 0:
                print("Incasso registrato")
                err_incasso = False
            else:
                raise ValueError
        except ValueError:
            print("Incasso inserito non valido")

    # Controlla duplicati per titolo
    for f in film:
        if f["titolo"] == nome:
            if f["anno"] == anno and f["incassi"] == incasso:
                print("Film già registrato in archivio")
                return
            else:
                nome = f"{nome}({anno})"
            break

    film.append({"titolo": nome, "anno": anno, "incassi": incasso})
    print(f"Film '{nome}' aggiunto con successo!")


def visualizza(film):
    print("-" * 30)
    print("    LA TUA COLLEZIONE DI FILM")
    print("-" * 30)
    if len(film) == 0:
        print("Nessun film in collezione")
    else:
        for i, f in enumerate(film):
            print(f"[{i}] {f['titolo']}:")
            for key in f:
                print(f"     {key.capitalize()}: {f[key]}")
            print()


def modifica(film):
    if len(film) == 0:
        print("Nessun film da modificare.")
        return

    visualizza(film)

    err_mod_id = True
    while err_mod_id:
        try:
            mod_id = int(input("Quale film vuoi modificare? (Inserisci l'indice): "))
            if 0 <= mod_id < len(film):
                err_mod_id = False
            else:
                raise ValueError
        except ValueError:
            print("Indice inserito non valido")

    err_nome = True
    while err_nome:
        nome = input("Inserisci il nuovo titolo del film: ").capitalize()
        if nome != "":
            err_nome = False
        else:
            print("Titolo vuoto non valido")

    err_anno = True
    while err_anno:
        try:
            anno = int(input("Inserisci il nuovo anno di uscita: "))
            if anno > 1895:
                err_anno = False
            else:
                raise ValueError
        except ValueError:
            print("Anno inserito non valido")

    err_incasso = True
    while err_incasso:
        try:
            incasso = float(input("Inserisci i nuovi incassi al botteghino: "))
            if incasso >= 0:
                err_incasso = False
            else:
                raise ValueError
        except ValueError:
            print("Incasso inserito non valido")

    film[mod_id] = {"titolo": nome, "anno": anno, "incassi": incasso}
    print(f"Film all'indice {mod_id} aggiornato con successo!")


def cancella(film):
    if len(film) == 0:
        print("Nessun film da eliminare.")
        return

    visualizza(film)

    err_rm_id = True
    while err_rm_id:
        try:
            mod_id = int(input("Quale film vuoi rimuovere? (Inserisci l'indice): "))
            if 0 <= mod_id < len(film):
                titolo = film[mod_id]["titolo"]
                film.pop(mod_id)
                print(f"Film '{titolo}' rimosso con successo!")
                err_rm_id = False
            else:
                raise ValueError
        except ValueError:
            print("Indice inserito non valido")


def salva(film):
    """Salva la collezione sia in CSV che in JSON."""
    # Salvataggio CSV
    try:
        with open(FILE_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=SEPARATORE)
            writer.writerow(["titolo", "anno", "incassi"])  # intestazione
            for entry in film:
                writer.writerow([entry["titolo"], entry["anno"], entry["incassi"]])
        print(f"Collezione salvata in '{FILE_CSV}'")
    except IOError as e:
        print(f"Errore nel salvataggio CSV: {e}")

    # Salvataggio JSON
    try:
        with open(FILE_JSON, "w", encoding="utf-8") as f:
            json.dump(film, f, ensure_ascii=False, indent=4)
        print(f"Collezione salvata in '{FILE_JSON}'")
    except IOError as e:
        print(f"Errore nel salvataggio JSON: {e}")


def carica():
    """
    Carica la collezione dal file JSON (priorità) o dal file CSV.
    Restituisce la lista dei film caricati, oppure una lista vuota.
    """
    if os.path.exists(FILE_JSON):
        try:
            with open(FILE_JSON, "r", encoding="utf-8") as f:
                dati = json.load(f)
            print(f"Collezione caricata da '{FILE_JSON}' ({len(dati)} film)")
            return dati
        except (IOError, json.JSONDecodeError) as e:
            print(f"Errore nel caricamento JSON: {e}")

    if os.path.exists(FILE_CSV):
        try:
            dati = []
            with open(FILE_CSV, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=SEPARATORE)
                for riga in reader:
                    dati.append({
                        "titolo": riga["titolo"],
                        "anno": int(riga["anno"]),
                        "incassi": float(riga["incassi"])
                    })
            print(f"Collezione caricata da '{FILE_CSV}' ({len(dati)} film)")
            return dati
        except (IOError, KeyError, ValueError) as e:
            print(f"Errore nel caricamento CSV: {e}")

    print("Nessun file di salvataggio trovato. Si parte con la collezione predefinita.")
    return None


def menu():
    dati_caricati = carica()
    if dati_caricati is not None:
        collezione = dati_caricati
    else:
        collezione = film

    in_esecuzione = True
    while in_esecuzione:
        print("\n" + "=" * 30)
        print("       LA TUA VIDEOTECA")
        print("=" * 30)
        print("1. Inserisci nuovo film")
        print("2. Visualizza collezione")
        print("3. Modifica film")
        print("4. Elimina film")
        print("5. Salva collezione")
        print("6. Esci")
        print("=" * 30)

        err_choice = True
        while err_choice:
            try:
                choice = int(input("Cosa vuoi fare (opz 1-6): "))
                if 1 <= choice <= 6:
                    err_choice = False
                else:
                    raise ValueError
            except ValueError:
                print("Scelta non valida, inserisci un numero tra 1 e 6")

        if choice == 1:
            inserisci(collezione)
        elif choice == 2:
            visualizza(collezione)
        elif choice == 3:
            modifica(collezione)
        elif choice == 4:
            cancella(collezione)
        elif choice == 5:
            salva(collezione)
        elif choice == 6:
            err_uscita = True
            while err_uscita:
                risposta = input("Vuoi salvare prima di uscire? (s/n): ").strip().lower()
                if risposta == "s":
                    salva(collezione)
                    err_uscita = False
                elif risposta == "n":
                    err_uscita = False
                else:
                    print("Risposta non valida, inserisci 's' oppure 'n'")
            print("Arrivederci!")
            in_esecuzione = False


menu()