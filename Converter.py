import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def embed_png_to_svg(png_path, svg_path):
    """Konvertiert das PNG durch Einbettung in eine SVG."""
    try:
        # Bildgröße auslesen
        with Image.open(png_path) as img:
            width, height = img.size
        
        # PNG als Base64 codieren
        with open(png_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # SVG-Inhalt erstellen
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{encoded_string}"/>
</svg>'''
        
        # SVG speichern
        with open(svg_path, "w", encoding="utf-8") as svg_file:
            svg_file.write(svg_content)
        return True
    except Exception as e:
        messagebox.showerror("Fehler", f"Konvertierung fehlgeschlagen:\n{e}")
        return False

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG zu SVG Konverter")
        self.root.geometry("450x200")
        self.root.resizable(False, False)
        
        self.png_path = ""

        # --- UI Elemente ---
        
        # Info-Label
        self.label_info = tk.Label(
            root, 
            text="Wähle eine PNG-Datei aus, um sie in eine SVG einzubetten.",
            pady=10
        )
        self.label_info.pack()

        # Button zur Dateiauswahl
        self.btn_select = tk.Button(
            root, 
            text="PNG-Datei auswählen", 
            command=self.select_file,
            bg="#3498db", 
            fg="white", 
            padx=10, 
            pady=5
        )
        self.btn_select.pack(pady=5)

        # Label für den ausgewählten Dateipfad
        self.label_file = tk.Label(
            root, 
            text="Keine Datei ausgewählt", 
            fg="gray",
            wraplength=400
        )
        self.label_file.pack(pady=5)

        # Konvertieren Button (am Anfang deaktiviert)
        self.btn_convert = tk.Button(
            root, 
            text="Als SVG speichern...", 
            command=self.convert_file,
            state=tk.DISABLED,
            bg="#2ecc71", 
            fg="white",
            padx=10, 
            pady=5
        )
        self.btn_convert.pack(pady=10)

    def select_file(self):
        # Dateidialog öffnen
        file_path = filedialog.askopenfilename(
            title="PNG auswählen",
            filetypes=[("PNG Bilder", "*.png")]
        )
        
        if file_path:
            self.png_path = file_path
            # Dateiname im Interface anzeigen
            self.label_file.config(text=os.path.basename(file_path), fg="black")
            # Konvertierungs-Button freischalten
            self.btn_convert.config(state=tk.NORMAL)

    def convert_file(self):
        if not self.png_path:
            return
        
        # Standard-Vorschlag für den neuen Dateinamen generieren
        default_svg_name = os.path.splitext(os.path.basename(self.png_path))[0] + ".svg"
        
        # Speicherort abfragen
        output_path = filedialog.asksaveasfilename(
            title="SVG speichern unter...",
            initialfile=default_svg_name,
            filetypes=[("SVG Vektorgrafik", "*.svg")],
            defaultextension=".svg"
        )
        
        if output_path:
            # Eigentliche Konvertierung starten
            success = embed_png_to_svg(self.png_path, output_path)
            if success:
                messagebox.showinfo("Erfolg", "Die SVG-Datei wurde erfolgreich erstellt!")
                # Reset für die nächste Datei
                self.png_path = ""
                self.label_file.config(text="Keine Datei ausgewählt", fg="gray")
                self.btn_convert.config(state=tk.DISABLED)

# Hauptprogramm starten
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()