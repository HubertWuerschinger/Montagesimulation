import streamlit as st
import json
import pandas as pd

st.markdown("# Werkzeugnisübersicht ⭐")
st.sidebar.markdown("# Werkzeugnisübersicht ⭐")

# Dateiname der Datenbank
database_filename = "werkzeugnis_database.json"

def display_ampel_color(werkzeugnis_data):
    # Überprüfe, ob die Untereinträge "Montage" und "Oberfläche" in Ordnung sind
    is_ok = all(
        item["Qualitätsprüfung"].get("Montage") == "i.O" and
        item["Qualitätsprüfung"].get("Oberfläche") == "i.O"
        for item in werkzeugnis_data
    )
    
    return "Grün" if is_ok else "Rot"

def display_werkzeugnis_results():
    # Laden der Werkzeugnisdaten aus der JSON-Datei
    werkzeugnis_data = []
    try:
        with open(database_filename, "r") as db:
            for line in db:
                werkzeugnis_info = json.loads(line)
                werkzeugnis_data.append(werkzeugnis_info)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("Die Datei konnte nicht geladen werden oder ist leer.")
        return

    # Wenn Daten vorhanden sind, diese in einer Tabelle anzeigen
    if werkzeugnis_data:
        df = pd.DataFrame(werkzeugnis_data)
        df.set_index("Kunde", inplace=True)  # Setzen des Index auf "Kunde"

        # Größere Schriftgröße für die Tabelle festlegen
        styled_df = df.style.set_properties(**{
            'font-size': '14pt',
            'font-family': 'Calibri'
        })
        st.dataframe(styled_df, use_container_width=True)

        # Anzeige der Ampelgrafik je nach Qualitätsstatus
        ampel_color = display_ampel_color(werkzeugnis_data)
        if ampel_color == "Grün":
            st.image("gruene_ampel.jpg", caption="Status: Alles in Ordnung")
        else:
            st.image("rote_ampel.jpg", caption="Status: Überprüfung erforderlich")
    else:
        st.write("Keine Werkzeugnisdaten vorhanden.")

if __name__ == '__main__':
    display_werkzeugnis_results()
