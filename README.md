Foundry Calculator
Ein Produktionsplaner für dein Factory-Spiel mit visueller Graphvisualisierung und Rezept-Editor.
⚠️ Status: Aktuell nur ein Prototyp - Das Repository wird noch aktiv aktualisiert. Features und Struktur können sich ändern.
Features

📊 Produktionsplaner - Visualisiere Produktionsgraphen mit Vis.js
🔧 Rezept-Editor - Erstelle und bearbeite Rezepte mit GUI
⚙️ Machine-Berechnung - Automatische Berechnung von benötigten Maschinen/Minern basierend auf Settings
🎨 Modernes UI - Schönes Frontend mit Echtzeit-Berechnung

Quick Start
1. Produktionsplaner starten
bashpython start_planner.py
Das startet automatisch:

FastAPI Backend auf http://127.0.0.1:8080
Frontend öffnet sich im Browser

Dann kannst du:

Ziele (Endprodukte) hinzufügen
Machine/Miner-Level einstellen
Den Produktionsgraph live sehen

2. Rezepte hinzufügen/bearbeiten
bashpython Factory_manager.py
Damit kannst du:

Neue Rezepte erstellen
Items definieren
Zutaten und Zeiten festlegen
Alles wird in JSON gespeichert

Dateistruktur
Foundry-Calculator/
├── start_planner.py          # 👈 Haupteinstieg für Production
├── Factory_manager.py        # 👈 Nur für Rezept-Bearbeitung
├── main.py                   # FastAPI Backend
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── backend/
│   └── data/
│       ├── items.json
│       ├── recipes.json
│       ├── machines.json
│       ├── miners.json
│       ├── purity.json
│       └── belts.json
└── LICENSE
Abhängigkeiten

Python 3.8+
FastAPI
Uvicorn
Tkinter (für Factory_manager.py)

Installation
bashpip install fastapi uvicorn
Tkinter ist meist schon installiert. Wenn nicht:

Ubuntu/Debian: sudo apt-get install python3-tk
macOS: Kommt mit Python
Windows: Kommt mit Python

Entwicklung
Aktuell wird dieses Repository noch aktiv weiterentwickelt. Wenn du ändern möchtest:

Starte Factory_manager.py um Rezepte zu bearbeiten
Starte start_planner.py um die Ergebnisse zu testen
JSON-Dateien in backend/data/ werden automatisch aktualisiert

Lizenz
MIT License - siehe LICENSE Datei
Nächste Schritte (geplant)

 Dark Mode
 Export als SVG/PNG
 Speichern von Plänen
 Multi-language Support
