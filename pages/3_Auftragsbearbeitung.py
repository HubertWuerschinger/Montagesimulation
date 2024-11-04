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

# Funktion zum Laden der Daten aus JSON-Dateien
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
    
    # Sicherstellen, dass die benötigten Felder vorhanden sind
    kunde = selected_data.get("Kunde", "Unbekannt")
    auftragsnummer = selected_data.get("Auftragsnummer", "N/A")
    bestelldatum_uhrzeit = selected_data.get("Bestelldatum und Uhrzeit", "N/A")
    aktuelle_dauer_uhrzeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zeitdifferenz = timedifference(bestelldatum_uhrzeit)
    current_varianten = selected_data.get("Variante nach Bestellung", "N/A")
    selected_quality_montage = selected_data.get("Qualitätsprüfung", {}).get("Montage", "N/A")
    selected_quality_oberflaeche = selected_data.get("Qualitätsprüfung", {}).get("Oberfläche", "N/A")
    current_Kundentakt = selected_data.get("Kundentakt", "N/A")
    
    # Neue Zeile für die CSV-Datei
    new_row = [kunde, auftragsnummer, bestelldatum_uhrzeit, aktuelle_dauer_uhrzeit, 
               zeitdifferenz, current_varianten, 
               f"Montage: {selected_quality_montage}, Oberfläche: {selected_quality_oberflaeche}", 
               current_Kundentakt]

    # Schreibe die Daten in die CSV-Datei im Anfügemodus
    with open(filename, 'a', newline='', encoding='ISO-8859-1') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(new_row)

# Funktion zur Berechnung der Zeitdifferenz
def timedifference(bestelldatum_uhrzeit):
    try:
        bestelldatum = datetime.datetime.strptime(bestelldatum_uhrzeit, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        time_difference = (now - bestelldatum).total_seconds()
        return int(time_difference)
    except ValueError:
        st.warning("Ungültiges Datum/Uhrzeit-Format für die Berechnung der Zeitdifferenz.")
        return "N/A"

# Funktion zur Anzeige des Timers für einen bestimmten Kundentakt
def display_timer(seconds):
    timer_placeholder = st.empty()
    for sec in range(seconds, 0, -1):
        timer_placeholder.markdown(f"<h2>{sec} Sekunden verbleibend</h2>", unsafe_allow_html=True)
        time.sleep(1)
    timer_placeholder.write("Zeit abgelaufen!")

# Funktion zur Anzeige des nächsten Timers und zur Aktualisierung der Seite
def show_next_order_timer():
    # Sicherstellen, dass es mehr Aufträge gibt
    if st.session_state.auftrag_index < len(bestellungen_data):
        auftrag = bestellungen_data[st.session_state.auftrag_index]
        kundentakt = int(auftrag.get("Kundentakt", 0))
        kunde = auftrag.get("Kunde", "Unbekannt")
        
        st.write(f"Timer für {kunde} - Kundentakt: {kundentakt} Sekunden")
        
        # Zeige den Timer und aktualisiere den Auftragsindex nach Ablauf
        display_timer(kundentakt)
        
        # Erhöhen des Zählers nach Ablauf des Timers
        st.session_state.auftrag_index += 1
        
        # Seite neu laden, um den Timer für den nächsten Auftrag zu starten
        st.experimental_rerun()
    else:
        st.write("Alle Aufträge wurden abgearbeitet.")

# Hauptlogik
# Laden der JSON-Daten für Bestellungen
bestellungen_data = load_existing_data(bestellungen_database_filename)

# Initialisieren des Session State für den Zähler
if 'auftrag_index' not in st.session_state:
    st.session_state.auftrag_index = 0

if bestellungen_data:
    show_next_order_timer()
else:
    st.info("Es sind derzeit keine Bestellungen vorhanden.")
