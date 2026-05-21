# Foundry Calculator

Ein Produktionsplaner für dein Factory-Spiel mit visueller Graphvisualisierung.

## Features
- Rezept-Editor (GUI) mit `Factory_manager.py`
- Produktionsplaner mit Vis.js-Diagrammen
- Machine/Miner-Berechnung basierend auf Einstellungen

## Setup

1. **Backend starten**
```bash
   pip install fastapi uvicorn
   python main.py
```
   Läuft auf: http://127.0.0.1:8000

2. **Frontend öffnen**
   Öffne `frontend/index.html` im Browser
   (Oder serve mit `python -m http.server` im frontend-Ordner)

3. **Rezepte bearbeiten**
   Starte `Factory_manager.py` zum Erstellen/Bearbeiten von Rezepten

## Dateistruktur
- `main.py` - FastAPI Backend
- `Factory_manager.py` - Tkinter GUI für Rezepte
- `frontend/` - HTML/CSS/JS Interface
- `backend/data/` - JSON Dateien (items, recipes, machines, etc.)

## Lizenz
MIT
