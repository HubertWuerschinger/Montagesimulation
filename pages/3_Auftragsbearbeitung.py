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

# Datenbank-Dateien im JSON-Format
werkzeugnis_database_filename = "werkzeugnis_database.json"
bestellungen_database_filename = "bestellungen_database.json"

# Funktion zum Laden der bestehenden Daten aus einer JSON-Datei
def load_existing_data(filename):
    try:
        with open(filename, "r") as file:
            data = [json.loads(line) for line in file]
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Funktion zum Speichern der Daten in einer CSV-Datei (Header wird vorausgesetzt)
def save_to_csv(selected_data):
    filename = "bearbeitsungsstatus.csv"
    
    # Füge die neue Zeile mit den aktuellen Daten hinzu
    kunde = selected_data["Kunde"]
    auftragsnummer = selected_data.get("Auftragsnummer", "N/A")
    bestelldatum_uhrzeit = selected_data["Bestelldatum"]
    aktuelle_dauer_uhrzeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zeitdifferenz = timedifference(selected_data["Bestelldatum"])
    current_varianten = selected_data["Variante nach Bestellung"]
    selected_quality_montage = selected_data["Qualitätsprüfung"].get("Montage", "N/A")
    selected_quality_oberflaeche = selected_data["Qualitätsprüfung"].get("Oberfläche", "N/A")
    current_Kundentakt = selected_data["Kundentakt"]
    new_row = [kunde, auftragsnummer, bestelldatum_uhrzeit, aktuelle_dauer_uhrzeit, 
               zeitdifferenz, current_varianten, 
               f"Montage: {selected_quality_montage}, Oberfläche: {selected_quality_oberflaeche}", 
               current_Kundentakt]

    # Schreibe die Daten in die CSV-Datei im Anfügemodus
    with open(filename, 'a', newline='', encoding='ISO-8859-1') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(new_row)

# Funktion zur strukturierten Anzeige des CSV-DataFrames in Streamlit
def display_csv():
    filename = "bearbeitsungsstatus.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename, encoding='ISO-8859-1')
        st.markdown("## Bearbeitungsstatus der abgeschlossenen Aufträge")
        st.write("Hier sehen Sie die aktuellen Aufträge, die abgeschlossen wurden und deren Bearbeitungsstatus.")
        
        # Formatierte Anzeige des DataFrames
        st.dataframe(
            df.style.set_properties(
                **{
                    'text-align': 'left',
                    'font-size': '12pt'
                }
            ).set_table_styles(
                [{'selector': 'th', 'props': [('font-size', '14pt'), ('text-align', 'left')]}]
            ),
            use_container_width=True
        )
    else:
        st.warning("Die Datei 'bearbeitsungsstatus.csv' wurde nicht gefunden oder enthält keine Daten.")

# Funktion für die Zeitdifferenzberechnung
def timedifference(current_datetime):
    bestelldatum = datetime.datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    time_difference = (now - bestelldatum).total_seconds()
    return int(time_difference)

# Laden der JSON-Daten für Bestellungen
bestellungen_data = load_existing_data(bestellungen_database_filename)

# Überprüfen, ob `bestellungen_data` Daten enthält
if bestellungen_data:
    # Erstellen einer Liste von Optionen für die selectbox mit Auftragsdatum und Kundenname
    selectbox_options = [f"{entry['Bestelldatum und Uhrzeit']} - {entry['Kunde']}" for entry in bestellungen_data]

    # Lassen Sie den Benutzer eine Bestellung auswählen
    selected_option = st.selectbox("Bestellung:", selectbox_options, 0)

    # Überprüfen, ob `selected_option` gültig ist, bevor wir fortfahren
    if selected_option in selectbox_options:
        # Extrahieren von Auftragsdatum und Kundenname aus der ausgewählten Option
        selected_index = selectbox_options.index(selected_option)
        selected_data = bestellungen_data[selected_index]
        current_datetime = selected_data["Bestelldatum und Uhrzeit"]
        current_Kunde = selected_data["Kunde"]

        # Restliche Daten extrahieren
        current_Sonderwunsch = selected_data.get("Sonderwunsch", "N/A")
        current_Varianten = selected_data.get("Variante nach Bestellung", "N/A")
        current_Kundentakt = selected_data.get("Kundentakt", "N/A")

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

        # Schaltfläche, um das Werkzeugnis zu generieren
        if st.button("Auftrag abgeschlossen und Bestellung zum Kunden verschickt"):
            # Aktualisieren der Qualitätsprüfung
            selected_data["Qualitätsprüfung"] = selected_quality

            # Speichern in JSON-Datei
            existing_data = load_existing_data(werkzeugnis_database_filename)
            existing_data.append(selected_data)
            with open(werkzeugnis_database_filename, "w") as db:
                for entry in existing_data:
                    db.write(json.dumps(entry) + "\n")

            time_diff = timedifference(current_datetime)  # Berechnen der Zeitdifferenz
            st.write(f"Der Kundenauftrag wurde in {time_diff} Sekunden bearbeitet")
            time.sleep(1)

            # Speichern in CSV-Datei
            save_to_csv(selected_data)

            # Zeige die aktualisierte CSV-Datei als Tabelle an
            display_csv()
else:
    st.info("Es sind derzeit keine Bestellungen vorhanden.")
