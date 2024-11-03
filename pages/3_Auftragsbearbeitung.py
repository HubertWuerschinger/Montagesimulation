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

# Datenbank-Datei für Werkzeugnisinformationen im JSON-Format
werkzeugnis_database_filename = "werkzeugnis_database.json"

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
    header = ["Kunde", "Auftragsnummer", "Bestelldatum Uhrzeit", "Aktuelle Dauer und Uhrzeit", 
              "Zeitdifferenz", "current varianten", "selected quality", "Kundentakt"]
    
    # Überprüfen, ob die Datei existiert und ob der Header korrekt ist
    file_exists = os.path.isfile(filename)
    if not file_exists:
        # Schreibe den Header, wenn die Datei neu erstellt wird
        with open(filename, 'w', newline='', encoding='ISO-8859-1') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
    
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
    new_row = [kunde, auftragsnummer, bestelldatum_uhrzeit, aktuelle_dauer_uhrzeit, 
               zeitdifferenz, current_varianten, f"Montage: {selected_quality_montage}, Oberfläche: {selected_quality_oberflaeche}", current_Kundentakt]

    # Schreibe die Daten in die CSV-Datei im Anfügemodus
    with open(filename, 'a', newline='', encoding='ISO-8859-1') as csvfile:
        csv_writer = csv.writer(csvfile)
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

# Restlicher Code für das Streamlit-Interface (ohne Änderungen) ...
