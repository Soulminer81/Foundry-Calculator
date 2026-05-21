# 🏭 Foundry Calculator

Ein **Produktionsplaner für dein Factory-Spiel** mit visueller Graphvisualisierung und Rezept-Editor. 
Automatisch berechne benötigte Maschinen/Miner und visualisiere deine komplexen Produktionsketten!

> ⚠️ **Status**: Aktuell nur ein Prototyp - Das Repository wird noch aktiv aktualisiert. Features und Struktur können sich ändern.

## 📋 Inhaltsverzeichnis

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [Tech-Stack](#tech-stack)
- [Entwicklung](#entwicklung)
- [Geplante Features](#geplante-features)
- [Lizenz](#lizenz)

## ✨ Features

- **📊 Produktionsplaner** - Visualisiere Produktionsgraphen mit [Vis.js](https://visjs.org/)
- **🔧 Rezept-Editor** - Erstelle und bearbeite Rezepte mit grafischer GUI
- **⚙️ Machine-Berechnung** - Automatische Berechnung von benötigten Maschinen/Minern basierend auf Settings
- **🎨 Modernes UI** - Schönes Frontend mit Echtzeit-Berechnung
- **💾 Persistente Daten** - JSON-basierte Speicherung für Rezepte und Konfigurationen

## 🚀 Quick Start

### 1️⃣ Produktionsplaner starten

```bash
python start_planner.py
```

Das startet automatisch:
- **FastAPI Backend** auf `http://127.0.0.1:8080`
- **Frontend** öffnet sich im Browser

Dann kannst du:
- ✅ Ziele (Endprodukte) hinzufügen
- ✅ Machine/Miner-Level einstellen
- ✅ Den Produktionsgraph live sehen

### 2️⃣ Rezepte hinzufügen/bearbeiten

```bash
python Factory_manager.py
```

Damit kannst du:
- ✅ Neue Rezepte erstellen
- ✅ Items definieren
- ✅ Zutaten und Zeiten festlegen
- ✅ Alles wird in JSON gespeichert

## 📦 Installation

### Voraussetzungen

- **Python 3.8+**
- Ein moderner Webbrowser (Chrome, Firefox, Edge, Safari)

### Schritt-für-Schritt

1. **Repository klonen**
   ```bash
   git clone https://github.com/Soulminer81/Foundry-Calculator.git
   cd Foundry-Calculator
   ```

2. **Dependencies installieren**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Tkinter installieren** (für Factory_manager.py)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install python3-tk
   ```
   
   **macOS & Windows:** Kommt automatisch mit Python ✓

4. **Fertig!** - Du kannst jetzt starten:
   ```bash
   python start_planner.py
   ```

## 📂 Projektstruktur

```
Foundry-Calculator/
├── start_planner.py           # 👈 Haupteinstieg für Production Planner
├── Factory_manager.py         # 👈 GUI für Rezept-Bearbeitung
├── main.py                    # FastAPI Backend
├── frontend/
│   ├── index.html             # Web-Interface
│   ├── app.js                 # Frontend-Logik
│   └── style.css              # Styling
├── backend/
│   └── data/
│       ├── items.json         # Item-Definitionen
│       ├── recipes.json       # Rezepte
│       ├── machines.json      # Maschinen-Daten
│       ├── miners.json        # Miner-Daten
│       ├── purity.json        # Reinheits-Level
│       └── belts.json         # Förderband-Daten
└── LICENSE
```

## 🛠 Tech-Stack

| Komponente | Technologie |
|-----------|------------|
| **Backend** | Python, FastAPI, Uvicorn |
| **Frontend** | HTML, CSS, JavaScript |
| **Visualisierung** | Vis.js |
| **Desktop GUI** | Tkinter |
| **Datenspeicherung** | JSON |

## 💻 Verwendung

### Produktionsplaner

1. **Starten:** `python start_planner.py`
2. **Browser öffnet sich automatisch** auf http://127.0.0.1:8080
3. **Items zur Zielproduktion hinzufügen**
4. **Machine/Miner-Level anpassen** → Berechnung erfolgt live
5. **Produktionsgraph visualisiert sich automatisch**

### Rezept-Editor

1. **Starten:** `python Factory_manager.py`
2. **GUI öffnet sich** mit Rezept-Verwaltung
3. **Neue Rezepte erstellen** oder bestehende anpassen
4. **Speichern** → JSON wird automatisch aktualisiert
5. **Neu laden im Planner** → Änderungen sind sofort verfügbar

## 🔧 Entwicklung

Wenn du Änderungen am Projekt vornehmen möchtest:

```bash
# 1. Repository klonen
git clone https://github.com/Soulminer81/Foundry-Calculator.git
cd Foundry-Calculator

# 2. Rezepte bearbeiten
python Factory_manager.py
# → Ändere Rezepte in der GUI
# → JSON-Dateien in backend/data/ werden automatisch aktualisiert

# 3. Ergebnisse testen
python start_planner.py
# → Der Planner lädt die aktualisierten Rezepte automatisch
```

### Datenquellen bearbeiten

Die JSON-Dateien in `backend/data/` sind die Single Source of Truth:
- `items.json` - Alle verfügbaren Items
- `recipes.json` - Herstellungsrezepte
- `machines.json` - Maschinentypen und Geschwindigkeiten
- `miners.json` - Miner-Typen und Erträge
- `purity.json` - Reinheits-Level Modifikatoren
- `belts.json` - Förderband-Kapazitäten

## 🎯 Geplante Features

- [ ] 🌙 Dark Mode
- [ ] 📥 Export als SVG/PNG
- [ ] 💾 Speichern von Plänen
- [ ] 🌍 Multi-language Support
- [ ] 📱 Mobile-optimiertes Interface
- [ ] 🔄 Undo/Redo Funktionalität

## 🤝 Beiträge

Beiträge sind willkommen! Bitte:

1. **Forke** das Repository
2. **Erstelle** einen Feature-Branch: `git checkout -b feature/AmazingFeature`
3. **Commite** deine Änderungen: `git commit -m 'Add some AmazingFeature'`
4. **Pushe** zum Branch: `git push origin feature/AmazingFeature`
5. **Öffne** einen Pull Request

## 📄 Lizenz

Dieses Projekt ist unter der **MIT License** lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

---

**Made with ❤️ by [Soulminer81](https://github.com/Soulminer81)**
