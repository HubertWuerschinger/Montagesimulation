import streamlit as st
import pandas as pd
import altair as alt
import os

# CSV-Datei
CSV_FILE = "bearbeitsungsstatus.csv"

# Erwartete Spaltennamen in der CSV-Datei (normalisiert)
EXPECTED_COLUMNS = ["kunde", "auftragsnummer", "bestelldatum uhrzeit", "aktuelle dauer und uhrzeit", 
                    "zeitdifferenz", "current varianten", "selected quality", "kundentakt"]

# Funktion zum Laden und Bereinigen der CSV-Datei
def load_data():
    try:
        if os.path.isfile(CSV_FILE):
            # Laden der CSV-Datei
            data = pd.read_csv(CSV_FILE, encoding='ISO-8859-1')
            
            # Normalisieren der Spaltennamen, um Abweichungen zu korrigieren
            data.columns = [col.strip().lower() for col in data.columns]
            st.write("Geladene Spalten nach Bereinigung:", data.columns.tolist())

            # Überprüfen, ob alle erwarteten Spalten vorhanden sind
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in data.columns]
            if missing_columns:
                st.warning(f"Die CSV-Datei hat fehlende oder abweichende Spalten: {missing_columns}")
            
            return data
        else:
            st.warning(f"Die Datei '{CSV_FILE}' wurde nicht gefunden.")
            return None
    except pd.errors.EmptyDataError:
        st.warning(f"Die Datei '{CSV_FILE}' ist leer.")
        return None

# Lade die Daten
data = load_data()

# Zeige die Daten in einer Tabelle an, falls sie existieren und nicht leer sind
if data is not None and not data.empty:
    st.markdown("## Erledigte Aufträge")
    st.write("Bearbeitungsstatus aus CSV-Datei:")
    st.dataframe(data, use_container_width=True)

    # Überprüfe, ob die erforderlichen Spalten für das Diagramm vorhanden sind
    if all(col in data.columns for col in ["kunde", "kundentakt", "zeitdifferenz"]):
        # Erstelle ein Balkendiagramm mit Altair, das die Aufträge nach Kundentakt und Bearbeitungszeit visualisiert
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('kunde:N', title='Kunde'),
            y=alt.Y('kundentakt:Q', title='Kundentakt'),
            color=alt.value('steelblue')
        ).properties(
            width=600,
            height=300
        )

        # Kombiniere das Diagramm für Kundentakt mit Bearbeitungszeit
        bearbeitung_chart = alt.Chart(data).mark_bar(color='orange').encode(
            x=alt.X('kunde:N', title='Kunde'),
            y=alt.Y('zeitdifferenz:Q', title='Bearbeitungszeit (Sekunden)')
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
