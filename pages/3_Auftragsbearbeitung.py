import streamlit as st
import datetime
import time
import json
import pandas as pd
import csv
import os

st.markdown("# Auftrag abschließen ✏️")
st.sidebar.markdown("# Auftrag abschließen ✏️")
st.write("Qualitätskontrolle und Versandt")

# Funktion zum Ermitteln der höchsten bisher verwendeten Werkzeugnisnummer
def get_highest_werkzeugnis_num(data):
    if not data:
        return 0
    return max(int(entry["Werkzeugnisnummer"]) for entry in data)

# Datenbank-Datei für Werkzeugnisinformationen im JSON-Format
werkzeugnis_database_filename = "werkzeugnis_database.json"

# Laden der bestehenden Werkzeugnisdaten aus der JSON-Datei
def load_existing_data(filename):
    try:
        with open(filename, "r") as file:
            data = [json.loads(line) for line in file]
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Funktion zum Speichern der Daten in einer CSV-Datei
def save_to_csv(data):
    filename = "bearbeitsungsstatus.csv"
    header = ["Kunde", "Auftragsnummer", "Bestelldatum Uhrzeit", "Aktuelle Dauer und Uhrzeit", "Zeitdifferenz", "current varianten", "selected quality", "Kundentakt"]
    rows = []

    # Wenn die Datei existiert, laden Sie die vorhandenen Daten
    if os.path.isfile(filename):
        with open(filename, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)  # Header-Zeile überspringen
            for row in csv_reader:
                rows.append(row)

    # Füge die neue Zeile hinzu
    kunde = data[0]["Kunde"]
    auftragsnummer = data[0].get("Auftragsnummer", "N/A")
    bestelldatum_uhrzeit = data[0]["Bestelldatum"]
    aktuelle_dauer_uhrzeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zeitdifferenz = timedifference(data[0]["Bestelldatum"])
    current_varianten = data[0]["Variante nach Bestellung"]
    selected_quality_montage = data[0]["Qualitätsprüfung"].get("Montage", "N/A")
    selected_quality_oberflaeche = data[0]["Qualitätsprüfung"].get("Oberfläche", "N/A")
    current_Kundentakt = data[0]["Kundentakt"]
    new_row = [kunde, auftragsnummer, bestelldatum_uhrzeit, aktuelle_dauer_uhrzeit, zeitdifferenz, current_varianten, f"Montage: {selected_quality_montage}, Oberfläche: {selected_quality_oberflaeche}", current_Kundentakt]
    rows.append(new_row)

    # Schreibe die Daten zurück in die CSV-Datei
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Schreibe die Kopfzeile
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

existing_data = load_existing_data(werkzeugnis_database_filename)

# Automatisches Einfügen des ausgewählten Bestelldatums und der Uhrzeit
bestellungen_database_filename = "bestellungen_database.json"
bestellungen_data = load_existing_data(bestellungen_database_filename)

# Erstellen einer Liste von Optionen für die selectbox mit Auftragsdatum und Kundenname
selectbox_options = [f"{entry['Bestelldatum und Uhrzeit']} - {entry['Kunde']}" for entry in bestellungen_data]

# Lassen Sie den Benutzer auswählen
selected_option = st.selectbox("Bestellung:", selectbox_options, 0)  # 0 ist der Standardindex

# Extrahieren von Auftragsdatum und Kundenname aus der ausgewählten Option
selected_index = selectbox_options.index(selected_option)
selected_datetime = bestellungen_data[selected_index]
current_datetime = selected_datetime["Bestelldatum und Uhrzeit"]
current_Kunde = selected_datetime["Kunde"]

# Restliche Daten extrahieren
current_Sonderwunsch = selected_datetime.get("Sonderwunsch", "N/A")
current_Varianten = selected_datetime.get("Variante nach Bestellung", "N/A")
current_Kundentakt = selected_datetime.get("Kundentakt", "N/A")

st.write(f"Bestellung vom: {current_datetime}")

st.write("Varianten:")
st.write("Kundenvariante:", current_Varianten)
sonderwunsch = st.text_input("Sonderwunsch", current_Sonderwunsch)

# Qualitätsprüfung
st.write("Qualitätsprüfung:")
pruefungen = ["Montage", "Oberfläche"]
qualitaet = ["i.O", "ni.O"]
selected_quality = {}

for pruefung in pruefungen:
    st.write(pruefung)
    selected_q = st.radio(f"Auswahl {pruefung}", qualitaet)
    if selected_q:
        selected_quality[pruefung] = selected_q

# Hinzufügen der Funktion für die Zeitdifferenz
def timedifference(current_datetime):
    bestelldatum = datetime.datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    time_difference = (now - bestelldatum).total_seconds()
    return int(time_difference)

# Schaltfläche, um das Werkzeugnis zu generieren
if st.button("Auftrag abgeschlossen und Bestellung zum Kunden verschickt"):
    werkzeugnis_info = {
        "Bestelldatum": current_datetime,
        "Kunde": current_Kunde,
        "Sonderwunsch": sonderwunsch,
        "Variante nach Bestellung": current_Varianten,
        "Qualitätsprüfung": selected_quality,
        "Kundentakt": current_Kundentakt
    }
    existing_data.append(werkzeugnis_info)  # Hinzufügen der neuen Daten zu den vorhandenen Daten

    with open(werkzeugnis_database_filename, "w") as db:
        for entry in existing_data:
            db.write(json.dumps(entry) + "\n")

    time_diff = timedifference(current_datetime)  # Berechnen der Zeitdifferenz
    st.write(f"Der Kundenauftrag wurde in {time_diff} Sekunden bearbeitet")
    time.sleep(1)

    df = pd.DataFrame(existing_data)
    df.set_index("Kunde", inplace=True)

    save_to_csv(existing_data)

    # Nutze `st.query_params()` anstelle von `st.experimental_rerun()`
    try:
        st.query_params()
    except Exception as e:
        st.write("Warnung: Die Abfrageparameter konnten nicht aktualisiert werden.")
