import streamlit as st
import json
import time
import pandas as pd

# JSON-Datei für die Aufträge
database_filename = "bestellungen_database.json"

def load_orders():
    """Lädt die Auftragsdaten aus der JSON-Datei."""
    bestellungen_data = []
    try:
        with open(database_filename, "r") as db:
            for line in db:
                bestellungen_info = json.loads(line)
                bestellungen_data.append(bestellungen_info)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("Die Datei konnte nicht geladen werden oder ist leer.")
    return bestellungen_data

def create_order_dataframe(bestellungen_data):
    """Erstellt einen DataFrame aus den Bestellungsdaten und gibt diesen zurück."""
    if not bestellungen_data:
        return None

    # Erstellen eines DataFrames mit den erforderlichen Spalten
    df = pd.DataFrame(columns=["Bestelldatum und Uhrzeit", "Kunde", "Auftragsnummer", "Sonderwunsch", 
                               "Führerhaus", "Sidepipes", "Container 1", "Container 2", "Container 3", 
                               "Container 4", "Kundentakt"])
    
    for idx, entry in enumerate(bestellungen_data, start=1):
        df.loc[idx] = [
            entry["Bestelldatum und Uhrzeit"],
            entry["Kunde"],
            entry["Auftragsnummer"],
            entry["Sonderwunsch"],
            entry["Variante nach Bestellung"].get("Führerhaus", "N/A"),
            entry["Variante nach Bestellung"].get("Sidepipes", "N/A"),
            entry["Variante nach Bestellung"].get("Container 1", "N/A"),
            entry["Variante nach Bestellung"].get("Container 2", "N/A"),
            entry["Variante nach Bestellung"].get("Container 3", "N/A"),
            entry["Variante nach Bestellung"].get("Container 4", "N/A"),
            entry["Kundentakt"]
        ]

    return df

def run_timer_for_order(kundentakt, kunde_name):
    """Führt einen Countdown für den Kundentakt eines Auftrags aus."""
    timer_placeholder = st.empty()
    for i in range(kundentakt, -1, -1):
        timer_placeholder.markdown(
            f"<strong><span style='font-size: 2em;'>Zeit bis zum Ausliefern von {kunde_name}: {i} Sekunden</span></strong>",
            unsafe_allow_html=True
        )
        time.sleep(1)
    timer_placeholder.empty()

def display_orders_horizontally(df):
    """Zeigt die Aufträge horizontal an und startet nacheinander Timer für jeden Auftrag."""
    if df is None:
        st.write("Keine Bestellungen vorhanden.")
        return

    # Anzeigen der Bestellungen als horizontaler Streifen
    columns = st.columns(len(df))
    for idx, col in enumerate(columns):
        col.subheader(f"Auftrag {idx + 1}")
        col.write(df.iloc[idx][["Kunde", "Auftragsnummer", "Bestelldatum und Uhrzeit", "Sonderwunsch"]])
        col.write(df.iloc[idx][["Führerhaus", "Sidepipes", "Container 1", "Container 2", "Container 3", "Container 4"]])
        col.write(f"Kundentakt: {df.iloc[idx]['Kundentakt']} Sekunden")

def process_orders():
    """Verarbeitet die Aufträge nacheinander und führt den Timer für jeden Auftrag aus."""
    bestellungen_data = load_orders()
    df = create_order_dataframe(bestellungen_data)

    if df is None:
        st.write("Keine Bestellungen vorhanden.")
        return

    # Timer für jeden Auftrag in Reihenfolge der Aufträge starten
    for idx, row in df.iterrows():
        kundentakt = int(row["Kundentakt"])
        kunde_name = row["Kunde"]

        # Timer starten
        run_timer_for_order(kundentakt, kunde_name)

        # JSON-Datei nach Ablauf jedes Timers neu laden
        bestellungen_data = load_orders()
        df = create_order_dataframe(bestellungen_data)

        # Anzeigen der aktuellen Aufträge nach jedem Neuladen
        display_orders_horizontally(df)

        # Stoppen, wenn alle Aufträge durchlaufen wurden
        if idx >= len(df) - 1:
            st.write("Alle Aufträge wurden verarbeitet.")
            break

if __name__ == '__main__':
    process_orders()
