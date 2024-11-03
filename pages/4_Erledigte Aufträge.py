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
    
    # Anzeige der Tabelle mit Spaltennamen als Header
    st.dataframe(data, use_container_width=True)

    # Erstelle ein Balkendiagramm mit Altair, das die Aufträge nach Kundentakt und Bearbeitungszeit visualisiert
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Kunde:N', title='Kunde'),
        y=alt.Y('Kundentakt:Q', title='Kundentakt'),
        color=alt.value('steelblue')
    ).properties(
        width=600,
        height=300
    )

    # Kombiniere das Diagramm für Kundentakt mit Bearbeitungszeit
    bearbeitung_chart = alt.Chart(data).mark_bar(color='orange').encode(
        x=alt.X('Kunde:N', title='Kunde'),
        y=alt.Y('Zeitdifferenz:Q', title='Bearbeitungszeit (Sekunden)')
    ).properties(
        width=600,
        height=300
    )

    combined_chart = alt.layer(chart, bearbeitung_chart).resolve_scale(
        y='independent'  # Separate Skalen für Kundentakt und Bearbeitungszeit
    )

    st.altair_chart(combined_chart, use_container_width=True)

else:
    st.info("Es gibt derzeit keine abgeschlossenen Aufträge, die angezeigt werden können.")
