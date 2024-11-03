import streamlit as st
import json
import time
import pandas as pd

# Setze Streamlit-Optionen in try-except-Blöcken, um Fehler durch veraltete Optionen zu vermeiden
try:
    # st.set_option('deprecation.showPyplotGlobalUse', False)  # Optional: für zukünftige Updates anpassbar
    st.set_option('deprecation.showfileUploaderEncoding', False)
except Exception as e:
    st.write("Warnung: Eine Konfigurationsoption wird nicht unterstützt und wurde übersprungen.")

st.markdown("# Aufträge 🚀")
st.sidebar.markdown("# Aufträge 🚀")

# Dateiname der Datenbank
database_filename = "bestellungen_database.json"

def cooling_highlight(val):
    colors = {
        'Blau': '#ACE5EE',
        'Gelb': '#FFFF00',
        'Rot': '#FF0000',
    }
    return f'background-color: {colors.get(val, "white")}'

def display_results():
    # Laden der Werkzeugnisdaten aus der JSON-Datei
    bestellungen_data = []
    with open(database_filename, "r") as db:
        for line in db:
            bestellungen_info = json.loads(line)
            bestellungen_data.append(bestellungen_info)

    # Wenn Daten vorhanden sind, diese in einer Tabelle anzeigen
    if bestellungen_data:
        # Erstellen eines leeren DataFrames mit den erforderlichen Spalten
        df = pd.DataFrame(columns=["Bestelldatum und Uhrzeit:", "Kunde:", "Auftragsnummer", "Sonderwunsch:", "Führerhaus:", "Sidepipes:", "Container 1:", "Container 2:", "Container 3:", "Container 4:", "Kundentakt"])
        
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
        
        st.dataframe(df.T, use_container_width=True)  # Transponieren des DataFrames und Anzeigen als Tabelle
        
        df["Kundentakt"] = df["Kundentakt"].apply(int)
        
        st.write("Wenn für bestimmte Bestandteile keine Farbangaben gemacht wurden, dann können diese frei gewählt werden")
        
        # Countdown-Timer für Kundentakt
        timer_placeholder = st.empty()
        for i in range(df["Kundentakt"].values[0], -1, -1):
            timer_text = f"<strong><span style='font-size: 2em;'>Zeit bis zum Ausliefern (Kundentakt): {i} Sekunden</span></strong>"
            timer_placeholder.markdown(timer_text, unsafe_allow_html=True)
            time.sleep(1)

        # Timer abgeschlossen
        timer_placeholder.empty()
        
    else:
        st.write("Keine Bestellungen vorhanden.")

if __name__ == '__main__':
    display_results()

# Verwende `st.experimental_set_query_params` mit einer Abfrage, um die Seite neu zu laden
try:
    st.experimental_set_query_params()
except Exception as e:
    st.write("Warnung: Experimentelle Funktion wird nicht unterstützt und wurde übersprungen.")
