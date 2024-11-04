import streamlit as st
import json
import time
import pandas as pd
import csv
import os

# CSV-Dateiname
CSV_FILE = "bearbeitsungsstatus.csv"

# JSON-Datei für die Aufträge (zum Füllen der CSV, falls nötig)
database_filename = "bestellungen_database.json"

def load_last_order_from_csv():
    """Lädt die letzte Zeile aus der CSV-Datei."""
    try:
        if os.path.isfile(CSV_FILE):
            df = pd.read_csv(CSV_FILE, encoding='ISO-8859-1')
            if not df.empty:
                last_order = df.iloc[-1]  # Letzte Zeile der CSV-Datei
                return last_order
        else:
            st.warning(f"Die Datei '{CSV_FILE}' wurde nicht gefunden.")
    except pd.errors.EmptyDataError:
        st.warning("Die CSV-Datei ist leer.")
    return None

def run_timer(kundentakt, kunde_name):
    """Führt einen Countdown für den Kundentakt aus und liest danach die CSV-Datei erneut."""
    timer_placeholder = st.empty()
    for i in range(int(kundentakt), -1, -1):
        timer_placeholder.markdown(
            f"<strong><span style='font-size: 2em;'>Zeit bis zum Ausliefern für {kunde_name}: {i} Sekunden</span></strong>",
            unsafe_allow_html=True
        )
        time.sleep(1)
    timer_placeholder.empty()

def display_last_order():
    """Zeigt die letzte Bestellung aus der CSV an und startet den Timer."""
    last_order = load_last_order_from_csv()
    if last_order is None:
        st.write("Keine Bestellungen vorhanden.")
        return

    # Zeigt die letzte Bestellung in einem DataFrame-Format an
    df = pd.DataFrame([last_order])
    st.markdown("## Letzte Bestellung")
    st.dataframe(df.T, use_container_width=True)

    # Timer für den Kundentakt der letzten Bestellung starten
    kundentakt = int(last_order["Kundentakt"])
    kunde_name = last_order["Kunde"]
    run_timer(kundentakt, kunde_name)

    # Nach dem Timer erneut die CSV-Datei laden und die nächste letzte Bestellung anzeigen
    display_last_order()

if __name__ == '__main__':
    display_last_order()
