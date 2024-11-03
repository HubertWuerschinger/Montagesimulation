import streamlit as st
import pandas as pd
import altair as alt
import os

# Header für die CSV-Datei festlegen
CSV_FILE = "bearbeitsungsstatus.csv"
CSV_HEADER = ["Kunde", "Auftragsnummer", "Bestelldatum Uhrzeit", "Aktuelle Dauer und Uhrzeit", "Zeitdifferenz", "current varianten", "selected quality", "Kundentakt"]

# Funktion zum Laden der Daten aus der CSV-Datei
def load_data():
    try:
        # Überprüfe, ob die Datei existiert und initialisiere den Header, falls nicht vorhanden
        if not os.path.isfile(CSV_FILE):
            with open(CSV_FILE, 'w', newline='', encoding='ISO-8859-1') as f:
                pd.DataFrame(columns=CSV_HEADER).to_csv(f, index=False)

        # Lade die CSV-Datei mit abgeschlossenen Aufträgen
        data = pd.read_csv(CSV_FILE, encoding='ISO-8859-1')
        return data
    except FileNotFoundError:
        st.warning(f"Die Datei '{CSV_FILE}' wurde nicht gefunden.")
        return None
    except pd.errors.EmptyDataError:
        st.warning(f"Die Datei '{CSV_FILE}' ist leer.")
        return None

# Lade die Daten der abgeschlossenen Aufträge
data = load_data()

# Zeige die Daten in einer Tabelle an, falls sie existieren
if data is not None and not data.empty:
    st.markdown("## Erledigte Aufträge")
    st.write("Bearbeitungsstatus aus CSV-Datei:")
    
    # Anzeige der Tabelle mit Spaltennamen als Header
    st.dataframe(data, use_container_width=True)

    # Datenvorschau zur Überprüfung
    st.write("Datenvorschau:")
    st.write(data.head())

    # Überprüfe, ob die erforderlichen Spalten vorhanden sind
    if all(col in data.columns for col in ["Kunde", "Kundentakt", "Zeitdifferenz"]):
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
        st.warning("Die erforderlichen Spalten 'Kunde', 'Kundentakt' und 'Zeitdifferenz' sind nicht in den Daten vorhanden.")
else:
    st.info("Es gibt derzeit keine abgeschlossenen Aufträge, die angezeigt werden können.")
