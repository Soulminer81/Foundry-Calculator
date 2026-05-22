import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import base64
from PIL import Image as PILImage

# Absolute Pfade zu deinem Unterordner aufbauen
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = os.path.join(BASE_PATH, 'backend', 'data', 'items.json')
RECIPES_FILE = os.path.join(BASE_PATH, 'backend', 'data', 'recipes.json')

# NEU: Der gewünschte Zielordner für deine SVG-Bilder
IMAGE_TARGET_DIR = r"C:\Users\staap\Desktop\Github\Foundry-Calculator\frontend\images"

# Variable zur temporären Speicherung des ausgewählten Bildpfads im aktuellen Workflow
selected_image_path = None

# --- DATEN LADEN & SPEICHERN ---
def load_data():
    items = {}
    recipes = {}
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
            items = json.load(f)
    if os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, 'r', encoding='utf-8') as f:
            recipes = json.load(f)
    return items, recipes

ITEMS, RECIPES = load_data()

def save_all_data():
    os.makedirs(os.path.dirname(ITEMS_FILE), exist_ok=True)
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ITEMS, f, ensure_ascii=False, indent=2)
    with open(RECIPES_FILE, 'w', encoding='utf-8') as f:
        json.dump(RECIPES, f, ensure_ascii=False, indent=2)

# --- BILD-KONVERTIERUNG (PNG -> SVG) ---
def save_png_as_svg(png_path, item_id):
    """
    Konvertiert ein PNG in ein SVG, indem das PNG als Base64 in das SVG eingebettet wird.
    Speichert das Ergebnis im definierten Zielordner unter dem Namen des Items.
    """
    try:
        os.makedirs(IMAGE_TARGET_DIR, exist_ok=True)
        target_svg_path = os.path.join(IMAGE_TARGET_DIR, f"{item_id}.svg")
        
        # Bildgröße ermitteln
        with PILImage.open(png_path) as img:
            width, height = img.size
            
        # PNG-Datei binär lesen und in Base64 kodieren
        with open(png_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
        # SVG-Inhalt mit eingebettetem Base64-String zusammenbauen
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
        svg_content += f'  <image xlink:href="data:image/png;base64,{encoded_string}" x="0" y="0" width="{width}" height="{height}"/>\n'
        svg_content += '</svg>'
        
        # SVG speichern
        with open(target_svg_path, "w", encoding="utf-8") as svg_file:
            svg_file.write(svg_content)
            
        return True
    except Exception as e:
        messagebox.showerror("Fehler bei Bildkonvertierung", f"Bild konnte nicht konvertiert werden:\n{str(e)}")
        return False

# --- UTILS ---
def generate_id(name):
    """Generiert eine standardisierte ID aus einem Klarnamen."""
    clean_id = name.lower().replace(" ", "_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return "".join([c for c in clean_id if c.isalnum() or c == "_"])

def get_id_by_name(name_to_find):
    for k, v in ITEMS.items():
        if v['name'].lower() == name_to_find.lower():
            return k
    return None

def refresh_dropdowns():
    names = sorted([v['name'] for v in ITEMS.values()])
    recipe_input_combobox['values'] = names
    if names:
        recipe_input_combobox.current(0)

# Temporäre Liste für das aktuelle Rezept
current_recipe_inputs = {}

def update_listbox():
    listbox_ingredients.delete(0, tk.END)
    for k, v in current_recipe_inputs.items():
        display_name = ITEMS[k]['name'] if k in ITEMS else k
        listbox_ingredients.insert(tk.END, f"{v}x {display_name}")

# --- BILD AUSWÄHLEN (AKTION) ---
def action_select_image(label_widget):
    global selected_image_path
    path = filedialog.askopenfilename(
        title="PNG Bild auswählen",
        filetypes=[("PNG Bilder", "*.png")]
    )
    if path:
        selected_image_path = path
        label_widget.config(text=os.path.basename(path), foreground="green")
    else:
        selected_image_path = None
        label_widget.config(text="Kein Bild ausgewählt", foreground="gray")

# --- AKTIONEN: REZEPTE ---
def action_add_ingredient_to_list():
    ing_name = recipe_input_combobox.get()
    ing_id = get_id_by_name(ing_name)
    
    if not ing_id: return
        
    try:
        qty = int(entry_recipe_input_qty.get())
        if qty <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("Warnung", "Menge muss eine Zahl größer als 0 sein.")
        return
        
    current_recipe_inputs[ing_id] = qty
    update_listbox()

def action_clear_ingredients():
    current_recipe_inputs.clear()
    listbox_ingredients.delete(0, tk.END)

def action_load_recipe():
    output_name = entry_recipe_output.get().strip()
    if not output_name:
        messagebox.showwarning("Fehler", "Bitte gib zuerst den Namen des Produkts ein, das du laden willst!")
        return

    output_id = get_id_by_name(output_name)
    if not output_id:
        output_id = generate_id(output_name)

    if output_id in RECIPES:
        recipe = RECIPES[output_id]
        
        entry_recipe_time.delete(0, tk.END)
        entry_recipe_time.insert(0, str(recipe['time']))
        combobox_recipe_type.set(recipe['type'])
        
        current_recipe_inputs.clear()
        for ing_id, qty in recipe['inputs'].items():
            current_recipe_inputs[ing_id] = qty
            
        update_listbox()
        messagebox.showinfo("Erfolg", f"Rezept für '{output_name}' wurde erfolgreich geladen!")
    else:
        messagebox.showinfo("Info", f"Kein bestehendes Rezept für '{output_name}' gefunden. Du kannst ein neues erstellen.")

def action_add_recipe():
    global selected_image_path
    output_name = entry_recipe_output.get().strip()
    if not output_name: 
        messagebox.showwarning("Fehler", "Bitte gib ein, für welches Produkt das Rezept sein soll.")
        return
        
    output_id = get_id_by_name(output_name)
    if not output_id:
        output_id = generate_id(output_name)
        
    try:
        rec_time = float(entry_recipe_time.get())
        if rec_time <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("Fehler", "Bitte gib eine gültige Zeit ein (z.B. 3.5).")
        return
        
    if not current_recipe_inputs:
        messagebox.showwarning("Fehler", "Füge dem Rezept zuerst Zutaten hinzu!")
        return
        
    # Falls ein Bild ausgewählt wurde, konvertieren und im neuen Pfad speichern
    if selected_image_path:
        success = save_png_as_svg(selected_image_path, output_id)
        if not success: return # Abbrechen bei Fehler

    if output_id not in ITEMS:
        ITEMS[output_id] = {
            "name": output_name,
            "image": f"images/{output_id}.svg"
        }
    elif selected_image_path:
        # Falls das Item schon existierte, aber ein neues Bild mitgegeben wurde
        ITEMS[output_id]["image"] = f"images/{output_id}.svg"
        
    RECIPES[output_id] = {
        "type": combobox_recipe_type.get(),
        "time": rec_time,
        "inputs": current_recipe_inputs.copy(),
        "outputs": {output_id: 1}
    }
    
    save_all_data()
    
    entry_recipe_output.delete(0, tk.END)
    entry_recipe_time.delete(0, tk.END)
    action_clear_ingredients()
    refresh_dropdowns()
    
    # Bild-Status zurücksetzen
    selected_image_path = None
    lbl_recipe_img_status.config(text="Kein Bild ausgewählt", foreground="gray")
    
    messagebox.showinfo("Erfolg", f"Rezept und Item für '{output_name}' erfolgreich gespeichert!")

# --- AKTIONEN FÜR ROHMATERIAL ---
def action_add_raw_material():
    global selected_image_path
    raw_name = entry_raw_name.get().strip()
    if not raw_name:
        messagebox.showwarning("Fehler", "Bitte gib einen Namen für das Rohmaterial ein.")
        return

    raw_id = get_id_by_name(raw_name)
    if not raw_id:
        raw_id = generate_id(raw_name)

    # Prüfen, ob es bereits existiert
    if raw_id in ITEMS and raw_id not in RECIPES and not selected_image_path:
        messagebox.showinfo("Info", f"Das Rohmaterial '{raw_name}' existiert bereits.")
        return
    elif raw_id in RECIPES:
        confirm = messagebox.askyesno("Achtung", f"'{raw_name}' besitzt bereits ein Rezept. Wenn du es als Rohmaterial speicherst, wird das Rezept GELÖSCHT (wichtig für Miner-Logik). Fortfahren?")
        if not confirm:
            return
        del RECIPES[raw_id]

    # Falls ein Bild ausgewählt wurde, konvertieren und speichern
    if selected_image_path:
        success = save_png_as_svg(selected_image_path, raw_id)
        if not success: return

    # In items.json eintragen
    ITEMS[raw_id] = {
        "name": raw_name,
        "image": f"images/{raw_id}.svg"
    }

    save_all_data()
    entry_raw_name.delete(0, tk.END)
    refresh_dropdowns()
    
    # Bild-Status zurücksetzen
    selected_image_path = None
    lbl_raw_img_status.config(text="Kein Bild ausgewählt", foreground="gray")
    
    messagebox.showinfo("Erfolg", f"Rohmaterial '{raw_name}' wurde erfolgreich hinzugefügt!")


# --- GUI LAYOUT ---
root = tk.Tk()
root.title("Foundry Produktions-Planer Editor")
root.geometry("580x560") # Leicht vergrößert für die Buttons

# Notebook für Tabs erstellen
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---- TAB 1: REZEPTE ----
tab_recipe = ttk.Frame(notebook)
notebook.add(tab_recipe, text=" Rezept-Editor ")

frame_recipe = ttk.LabelFrame(tab_recipe, text=" Rezept hinzufügen / bearbeiten ", padding=15)
frame_recipe.pack(fill="both", expand=True, padx=10, pady=10)

# Zeile 0: Ziel-Produkt Textfeld + LADEN BUTTON
ttk.Label(frame_recipe, text="Rezept für:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
entry_recipe_output = ttk.Entry(frame_recipe, width=22)
entry_recipe_output.grid(row=0, column=1, columnspan=2, sticky="w", pady=5, padx=5)

btn_load_recipe = ttk.Button(frame_recipe, text="Rezept laden", command=action_load_recipe)
btn_load_recipe.grid(row=0, column=3, sticky="e", pady=5, padx=5)

# Zeile 1: Zeit & Maschine
ttk.Label(frame_recipe, text="Zeit (Sek):").grid(row=1, column=0, sticky="w", pady=5)
entry_recipe_time = ttk.Entry(frame_recipe, width=8)
entry_recipe_time.grid(row=1, column=1, sticky="w", pady=5, padx=5)

ttk.Label(frame_recipe, text="Maschine:").grid(row=1, column=2, sticky="w", pady=5)
combobox_recipe_type = ttk.Combobox(frame_recipe, values=["assembling", "smelting", "crushing", "fluidassembler"], state="readonly", width=12)
combobox_recipe_type.set("assembling")
combobox_recipe_type.grid(row=1, column=3, sticky="w", pady=5, padx=5)

# NEU - Zeile 2: Bild hinzufügen für Rezept-Produkt
ttk.Label(frame_recipe, text="PNG Bild (opt):").grid(row=2, column=0, sticky="w", pady=5)
btn_recipe_img = ttk.Button(frame_recipe, text="Bild wählen...", command=lambda: action_select_image(lbl_recipe_img_status))
btn_recipe_img.grid(row=2, column=1, sticky="w", pady=5, padx=5)
lbl_recipe_img_status = ttk.Label(frame_recipe, text="Kein Bild ausgewählt", foreground="gray")
lbl_recipe_img_status.grid(row=2, column=2, columnspan=2, sticky="w", pady=5, padx=5)

# Trennlinie (verschoben auf Row 3)
ttk.Separator(frame_recipe, orient="horizontal").grid(row=3, column=0, columnspan=4, sticky="ew", pady=10)

# Zeile 4: Zutaten hinzufügen
frame_ing_input = ttk.Frame(frame_recipe)
frame_ing_input.grid(row=4, column=0, columnspan=4, sticky="ew", pady=5)

ttk.Label(frame_ing_input, text="Zutat:").pack(side="left")
recipe_input_combobox = ttk.Combobox(frame_ing_input, state="readonly", width=18)
recipe_input_combobox.pack(side="left", padx=5)

ttk.Label(frame_ing_input, text="Anzahl:").pack(side="left")
entry_recipe_input_qty = ttk.Entry(frame_ing_input, width=5)
entry_recipe_input_qty.insert(0, "1")
entry_recipe_input_qty.pack(side="left", padx=5)

btn_add_ing = ttk.Button(frame_ing_input, text="+ Zutat", command=action_add_ingredient_to_list)
btn_add_ing.pack(side="left", padx=5)

# Zeile 5: Zutaten Liste
listbox_ingredients = tk.Listbox(frame_recipe, height=4)
listbox_ingredients.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=5)

btn_clear_ing = ttk.Button(frame_recipe, text="Leeren", command=action_clear_ingredients)
btn_clear_ing.grid(row=5, column=3, sticky="n", pady=5, padx=5)

# Zeile 6: Speichern Button
btn_save_recipe = ttk.Button(frame_recipe, text="Rezept & Bild dauerhaft speichern", command=action_add_recipe)
btn_save_recipe.grid(row=6, column=0, columnspan=4, sticky="ew", pady=10)


# ---- TAB 2: ROHMATERIAL ----
tab_raw = ttk.Frame(notebook)
notebook.add(tab_raw, text=" Rohmaterial hinzufügen ")

frame_raw = ttk.LabelFrame(tab_raw, text=" Neues Rohmaterial registrieren ", padding=15)
frame_raw.pack(fill="both", expand=True, padx=10)

ttk.Label(frame_raw, text="Warum hier eintragen?", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
info_text = (
    "Items, die hier hinzugefügt werden, benötigen kein Rezept.\n"
    "Das Backend (FastAPI) erkennt diese automatisch als 'Miner-Ressourcen'\n"
    "und berechnet dafür die benötigte Anzahl an Minern anstatt Fabriken."
)
ttk.Label(frame_raw, text=info_text, justify="left", foreground="gray").pack(anchor="w", pady=5)

ttk.Separator(frame_raw, orient="horizontal").pack(fill="x", pady=15)

# Eingabe-Bereich für Rohmaterial
frame_raw_input = ttk.Frame(frame_raw)
frame_raw_input.pack(fill="x", pady=5)

ttk.Label(frame_raw_input, text="Name des Rohstoffs: ", font=("Arial", 10)).pack(side="left", padx=5)
entry_raw_name = ttk.Entry(frame_raw_input, width=25)
entry_raw_name.pack(side="left", padx=5)

# NEU: Bild-Bereich für Rohmaterial
frame_raw_image = ttk.Frame(frame_raw)
frame_raw_image.pack(fill="x", pady=10)

ttk.Label(frame_raw_image, text="PNG Bild (opt): ", font=("Arial", 10)).pack(side="left", padx=5)
btn_raw_img = ttk.Button(frame_raw_image, text="Bild wählen...", command=lambda: action_select_image(lbl_raw_img_status))
btn_raw_img.pack(side="left", padx=5)
lbl_raw_img_status = ttk.Label(frame_raw_image, text="Kein Bild ausgewählt", foreground="gray")
lbl_raw_img_status.pack(side="left", padx=5)

btn_save_raw = ttk.Button(frame_raw, text="Rohmaterial & Bild dauerhaft speichern", command=action_add_raw_material)
btn_save_raw.pack(fill="x", pady=20)


# --- INITIALISIERUNG ---
refresh_dropdowns()
root.mainloop()