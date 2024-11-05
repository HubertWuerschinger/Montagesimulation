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

# JSON-Dateien für die Datenbanken
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

# Funktion zum Speichern der ausgewählten Daten in einer CSV-Datei (Header wird vorausgesetzt)
def save_to_csv(selected_data):
    filename = "bearbeitsungsstatus.csv"
    
    # Extrahiere die erforderlichen Daten für die CSV-Datei
    kunde = selected_data.get("Kunde", "Unbekannt")
    auftragsnummer = selected_data.get("Auftragsnummer", "N/A")
    bestelldatum_uhrzeit = selected_data.get("Bestelldatum und Uhrzeit", "N/A")  # Einheitliche Benennung
    aktuelle_dauer_uhrzeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zeitdifferenz = timedifference(bestelldatum_uhrzeit)
    current_varianten = selected_data.get("Variante nach Bestellung", "N/A")
    selected_quality_montage = selected_data.get("Qualitätsprüfung", {}).get("Montage", "N/A")
    selected_quality_oberflaeche = selected_data.get("Qualitätsprüfung", {}).get("Oberfläche", "N/A")
    current_Kundentakt = selected_data.get("Kundentakt", "N/A")
    
    new_row = [
        kunde, auftragsnummer, bestelldatum_uhrzeit, aktuelle_dauer_uhrzeit,
        zeitdifferenz, current_varianten,
        f"Montage: {selected_quality_montage}, Oberfläche: {selected_quality_oberflaeche}",
        current_Kundentakt
    ]

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
def timedifference(bestelldatum_uhrzeit):
    try:
        # Überprüfen, ob das Datumsformat korrekt ist
        bestelldatum = datetime.datetime.strptime(bestelldatum_uhrzeit, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        time_difference = (now - bestelldatum).total_seconds()
        return int(time_difference)
    except (ValueError, TypeError):
        st.warning("Ungültiges Datum/Uhrzeit-Format oder fehlendes Datum für die Berechnung der Zeitdifferenz.")
        return "N/A"

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
        # Extrahieren des Index der ausgewählten Bestellung
        selected_index = selectbox_options.index(selected_option)
        selected_data = bestellungen_data[selected_index]

        # Extrahieren von Auftragsdaten aus `selected_data`
        current_datetime = selected_data.get("Bestelldatum und Uhrzeit", "N/A")  # Einheitliche Benennung
        current_Kunde = selected_data.get("Kunde", "Unbekannt")
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
            selected_q = st.radio(f"Auswahl {pruefung}", qualitaet, key=pruefung)
            if selected_q:
                selected_quality[pruefung] = selected_q

        # Schaltfläche, um das Werkzeugnis zu generieren
        if st.button("Auftrag abgeschlossen und Bestellung zum Kunden verschickt"):
            # Aktualisieren der Qualitätsprüfung im ausgewählten Auftrag
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
