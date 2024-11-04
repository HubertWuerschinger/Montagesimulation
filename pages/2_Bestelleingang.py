import streamlit as st
import json
import time
import pandas as pd

# JSON-Datei für die Aufträge
database_filename = "bestellungen_database.json"

# Set zur Speicherung der bereits geladenen Auftragsnummern
loaded_orders = set()

def load_last_order():
    """Lädt die letzte Auftragszeile aus der JSON-Datei, die noch nicht angezeigt wurde."""
    try:
        with open(database_filename, "r") as db:
            lines = db.readlines()
            for line in reversed(lines):  # Rückwärts durch die Datei, um den neuesten nicht geladenen Auftrag zu finden
                order = json.loads(line)
                auftragsnummer = order.get("Auftragsnummer")
                if auftragsnummer and auftragsnummer not in loaded_orders:
                    loaded_orders.add(auftragsnummer)  # Markiere den Auftrag als geladen
                    return order
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
            f"<strong><span style='font-size: 3em; color: #333;'>Zeit bis zum Ausliefern für {kunde_name}: {i} Sekunden</span></strong>",
            unsafe_allow_html=True
        )
        time.sleep(1)
    timer_placeholder.empty()
    
    # Nach Ablauf des Timers die nächste Bestellung anzeigen
    display_last_order()

def display_last_order():
    """Zeigt die nächste nicht angezeigte Bestellung an und startet den Timer."""
    last_order = load_last_order()
    if not last_order:
        st.write("Keine neuen Bestellungen vorhanden.")
        return

    # DataFrame aus der letzten Bestellung erstellen und anzeigen
    df = create_order_dataframe(last_order)
    if df is not None:
        st.markdown("## Nächste Bestellung")
        
        # Größere Schriftgröße für die Tabelle festlegen
        styled_df = df.T.style.set_properties(**{
            'font-size': '20pt',  # Vergrößerte Schriftgröße für die Zellen
            'text-align': 'left'
        }).set_table_styles([
            {'selector': 'th', 'props': [('font-size', '22pt'), ('text-align', 'left')]}  # Größere Schrift für die Kopfzeilen
        ])
        
        st.dataframe(styled_df, use_container_width=True)  # Transponierte Darstellung für kompakte Anzeige

        # Timer für den Kundentakt der Bestellung starten
        kundentakt = int(df["Kundentakt"].iloc[0])
        kunde_name = df["Kunde"].iloc[0]
        run_timer(kundentakt, kunde_name)

if __name__ == '__main__':
    display_last_order()
