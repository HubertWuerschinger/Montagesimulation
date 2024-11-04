import streamlit as st
import datetime
import time
import json
import pandas as pd
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

# Timer-Anzeige für einen bestimmten Kundentakt
def display_timer(seconds):
    timer_placeholder = st.empty()
    for sec in range(seconds, 0, -1):
        timer_placeholder.markdown(f"<h2>{sec} Sekunden verbleibend</h2>", unsafe_allow_html=True)
        time.sleep(1)
    timer_placeholder.write("Zeit abgelaufen!")

# Laden der Bestelldaten
bestellungen_data = load_existing_data(bestellungen_database_filename)

# Initialisieren des Session State für den Zähler
if 'auftrag_index' not in st.session_state:
    st.session_state.auftrag_index = 0

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
if bestellungen_data:
    show_next_order_timer()
else:
    st.info("Es sind derzeit keine Bestellungen vorhanden.")
