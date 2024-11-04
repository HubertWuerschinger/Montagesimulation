import streamlit as st
import json
import time
import pandas as pd

# Streamlit-Optionen setzen
try:
    st.set_option('deprecation.showfileUploaderEncoding', False)
except Exception:
    pass

st.markdown("# Aufträge 🚀")
st.sidebar.markdown("# Aufträge 🚀")

# Dateiname der Datenbank
database_filename = "bestellungen_database.json"

def load_orders():
    """Lädt die Auftragsdaten aus der JSON-Datei."""
    bestellungen_data = []
    with open(database_filename, "r") as db:
        for line in db:
            bestellungen_info = json.loads(line)
            bestellungen_data.append(bestellungen_info)
    return bestellungen_data

def display_orders(bestellungen_data):
    """Zeigt die Bestellungen in einer Tabelle an und gibt einen DataFrame zurück."""
    if not bestellungen_data:
        st.write("Keine Bestellungen vorhanden.")
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

    st.dataframe(df.T, use_container_width=True)
    return df

def run_timer_for_orders(df):
    """Führt einen Timer für jeden Auftrag in der Reihenfolge des Kundentakts aus."""
    timer_placeholder = st.empty()

    for index, row in df.iterrows():
        kundentakt = int(row["Kundentakt"])
        for i in range(kundentakt, -1, -1):
            timer_placeholder.markdown(f"<strong><span style='font-size: 2em;'>Zeit bis zum Ausliefern (Kundentakt): {i} Sekunden</span></strong>", unsafe_allow_html=True)
            time.sleep(1)
        # Timer abgeschlossen
        timer_placeholder.empty()
        st.write(f"Auftrag von Kunde {row['Kunde']} abgeschlossen.")

        # JSON-Datei erneut laden und nächste Bestellung verwenden, falls vorhanden
        bestellungen_data = load_orders()
        df = display_orders(bestellungen_data)
        if df is None or index >= len(df):
            st.write("Keine weiteren Aufträge vorhanden.")
            break

if __name__ == '__main__':
    bestellungen_data = load_orders()
    df = display_orders(bestellungen_data)
    if df is not None:
        run_timer_for_orders(df)
