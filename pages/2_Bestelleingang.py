import streamlit as st
import json
import time
import pandas as pd

# JSON-Datei für die Aufträge
database_filename = "bestellungen_database.json"

def load_last_order():
    """Lädt die letzte Auftragszeile aus der JSON-Datei."""
    try:
        with open(database_filename, "r") as db:
            lines = db.readlines()
            if lines:
                last_order = json.loads(lines[-1])  # Nur die letzte Zeile laden
                return last_order
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("Die Datei konnte nicht geladen werden oder ist leer.")
    return None

def create_order_dataframe(order_data):
    """Erstellt einen DataFrame aus einem einzelnen Auftragsdatensatz."""
    if not order_data:
        return None

    # DataFrame für die letzte Bestellung erstellen
    df = pd.DataFrame([{
        "Bestelldatum und Uhrzeit": order_data.get("Bestelldatum und Uhrzeit"),
        "Kunde": order_data.get("Kunde"),
        "Auftragsnummer": order_data.get("Auftragsnummer"),
        "Sonderwunsch": order_data.get("Sonderwunsch"),
        "Führerhaus": order_data.get("Variante nach Bestellung", {}).get("Führerhaus", "N/A"),
        "Sidepipes": order_data.get("Variante nach Bestellung", {}).get("Sidepipes", "N/A"),
        "Container 1": order_data.get("Variante nach Bestellung", {}).get("Container 1", "N/A"),
        "Container 2": order_data.get("Variante nach Bestellung", {}).get("Container 2", "N/A"),
        "Container 3": order_data.get("Variante nach Bestellung", {}).get("Container 3", "N/A"),
        "Container 4": order_data.get("Variante nach Bestellung", {}).get("Container 4", "N/A"),
        "Kundentakt": order_data.get("Kundentakt", 0)
    }])
    
    return df

def run_timer(kundentakt, kunde_name):
    """Führt einen Countdown für den Kundentakt der letzten Bestellung aus und lädt danach die Daten erneut."""
    timer_placeholder = st.empty()
    for i in range(int(kundentakt), -1, -1):
        timer_placeholder.markdown(
            f"<strong><span style='font-size: 2em;'>Zeit bis zum Ausliefern für {kunde_name}: {i} Sekunden</span></strong>",
            unsafe_allow_html=True
        )
        time.sleep(1)
    timer_placeholder.empty()
    
    # Nach Ablauf des Timers erneut die Daten anzeigen
    display_last_order()

def display_last_order():
    """Zeigt die letzte Bestellung an und startet den Timer."""
    last_order = load_last_order()
    if not last_order:
        st.write("Keine Bestellungen vorhanden.")
        return

    # DataFrame aus der letzten Bestellung erstellen und anzeigen
    df = create_order_dataframe(last_order)
    if df is not None:
        st.markdown("## Letzte Bestellung")
        st.dataframe(df.T, use_container_width=True)  # Transponierte Darstellung für kompakte Anzeige

        # Timer für den Kundentakt der letzten Bestellung starten
        kundentakt = int(df["Kundentakt"].iloc[0])
        kunde_name = df["Kunde"].iloc[0]
        run_timer(kundentakt, kunde_name)

if __name__ == '__main__':
    display_last_order()
