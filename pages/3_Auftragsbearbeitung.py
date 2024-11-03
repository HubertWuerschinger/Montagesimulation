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

# Funktion zum Laden der bestehenden Werkzeugnisdaten aus der JSON-Datei
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
    
    # Überprüfen, ob die Datei existiert
    file_exists = os.path.isfile(filename)

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

    # Schreibe die Daten in die CSV-Datei, füge den Header nur hinzu, wenn die Datei neu erstellt wird
    with open(filename, 'a', newline='', encoding='ISO-8859-1') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not file_exists:
            csv_writer.writerow(header)  # Schreibe Header nur, wenn die Datei neu ist
        csv_writer.writerow(new_row)

# Funktion zum Laden der CSV-Datei und Anzeige der Tabelle
def display_csv():
    filename = "bearbeitsungsstatus.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename, encoding='ISO-8859-1')
        st.write("Aktualisierte Bearbeitungsstatus-Tabelle:")
        st.dataframe(df)
    else:
        st.write("Keine Daten zum Anzeigen.")

# Laden der JSON-Daten für Bestellungen
bestellungen_database_filename = "bestellungen_database.json"
bestellungen_data = load_existing_data(bestellungen_database_filename)

# Überprüfen, ob `bestellungen_data` Daten enthält
if bestellungen_data:
    # Erstellen einer Liste von Optionen für die selectbox mit Auftragsdatum und Kundenname
    selectbox_options = [f"{entry['Bestelldatum und Uhrzeit']} - {entry['Kunde']}" for entry in bestellungen_data]

    # Lassen Sie den Benutzer auswählen
    selected_option = st.selectbox("Bestellung:", selectbox_options, 0)

    # Überprüfen, ob `selected_option` gültig ist, bevor wir fortfahren
    if selected_option in selectbox_options:
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

        # Funktion für die Zeitdifferenz
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
            existing_data = load_existing_data(werkzeugnis_database_filename)
            existing_data.append(werkzeugnis_info)

            with open(werkzeugnis_database_filename, "w") as db:
                for entry in existing_data:
                    db.write(json.dumps(entry) + "\n")

            time_diff = timedifference(current_datetime)  # Berechnen der Zeitdifferenz
            st.write(f"Der Kundenauftrag wurde in {time_diff} Sekunden bearbeitet")
            time.sleep(1)

            save_to_csv(existing_data)

            # Zeige die aktualisierte CSV-Datei als Tabelle an
            display_csv()
else:
    st.info("Es sind derzeit keine Bestellungen vorhanden.")
