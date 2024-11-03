import streamlit as st
import pandas as pd
import altair as alt

# Funktion zum Laden der Daten aus der CSV-Datei
def load_data():
    try:
        # Lädt die CSV-Datei mit abgeschlossenen Aufträgen
        data = pd.read_csv("bearbeitsungsstatus.csv", encoding='ISO-8859-1')
        return data
    except FileNotFoundError:
        st.warning("Die Datei 'bearbeitsungsstatus.csv' wurde nicht gefunden.")
        return None
    except pd.errors.EmptyDataError:
        st.warning("Die Datei 'bearbeitsungsstatus.csv' ist leer.")
        return None

# Lade die Daten der abgeschlossenen Aufträge
data = load_data()

# Zeige die Daten in einer Tabelle an, falls sie existieren
if data is not None:
    st.markdown("## Erledigte Aufträge")
    st.write("Bearbeitungsstatus aus CSV-Datei:")
    st.dataframe(data)

    # Erstelle ein Balkendiagramm mit Altair, das die Aufträge visualisiert
    chart = alt.Chart(data).mark_bar().encode(
        x='Kunde:N',
        y='Zeitdifferenz:Q',
        color=alt.value('steelblue')
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Es gibt derzeit keine abgeschlossenen Aufträge, die angezeigt werden können.")
