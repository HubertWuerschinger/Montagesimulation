import streamlit as st
import json
import pandas as pd

# Dateiname der Datenbank
database_filename = "werkzeugnis_database.json"

def display_werkzeugnis_results():
    st.title("Anzeigen der Werkzeugnis Ergebnisse")

    # Laden der Werkzeugnisdaten aus der JSON-Datei
    werkzeugnis_data = []
    with open(database_filename, "r") as db:
        for line in db:
            werkzeugnis_info = json.loads(line)
            werkzeugnis_data.append(werkzeugnis_info)

    # Wenn Daten vorhanden sind, diese in einer Tabelle anzeigen
    if werkzeugnis_data:
        st.write("Werkzeugnisdaten:")
        df = pd.DataFrame(werkzeugnis_data)
        st.dataframe(df)
    else:
        st.write("Keine Werkzeugnisdaten vorhanden.")

if __name__ == '__main__':
    display_werkzeugnis_results()