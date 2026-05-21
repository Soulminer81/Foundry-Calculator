import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Absolute Pfade zu deinem Unterordner aufbauen
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = os.path.join(BASE_PATH, 'backend', 'data', 'items.json')
RECIPES_FILE = os.path.join(BASE_PATH, 'backend', 'data', 'recipes.json')

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

# --- GUI AKTIONEN ---
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
        # Falls die Zutat in items.json ist, nimm den Klarnamen, sonst die ID
        display_name = ITEMS[k]['name'] if k in ITEMS else k
        listbox_ingredients.insert(tk.END, f"{v}x {display_name}")

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

# NEU: Aktion zum Laden eines bestehenden Rezepts
def action_load_recipe():
    output_name = entry_recipe_output.get().strip()
    if not output_name:
        messagebox.showwarning("Fehler", "Bitte gib zuerst den Namen des Produkts ein, das du laden willst!")
        return

    # ID ermitteln (entweder über den Klarnamen oder direkt generiert)
    output_id = get_id_by_name(output_name)
    if not output_id:
        output_id = output_name.lower().replace(" ", "_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        output_id = "".join([c for c in output_id if c.isalnum() or c == "_"])

    if output_id in RECIPES:
        recipe = RECIPES[output_id]
        
        # 1. Typ & Zeit setzen
        entry_recipe_time.delete(0, tk.END)
        entry_recipe_time.insert(0, str(recipe['time']))
        combobox_recipe_type.set(recipe['type'])
        
        # 2. Zutaten laden
        current_recipe_inputs.clear()
        for ing_id, qty in recipe['inputs'].items():
            current_recipe_inputs[ing_id] = qty
            
        update_listbox()
        messagebox.showinfo("Erfolg", f"Rezept für '{output_name}' wurde erfolgreich geladen!")
    else:
        messagebox.showinfo("Info", f"Kein bestehendes Rezept für '{output_name}' gefunden. Du kannst ein neues erstellen.")

# Aktion: Rezept Speichern
def action_add_recipe():
    output_name = entry_recipe_output.get().strip()
    if not output_name: 
        messagebox.showwarning("Fehler", "Bitte gib ein, für welches Produkt das Rezept sein soll.")
        return
        
    output_id = get_id_by_name(output_name)
    if not output_id:
        output_id = output_name.lower().replace(" ", "_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        output_id = "".join([c for c in output_id if c.isalnum() or c == "_"])
        
    try:
        rec_time = float(entry_recipe_time.get())
        if rec_time <= 0: raise ValueError
    except ValueError:
        messagebox.showwarning("Fehler", "Bitte gib eine gültige Zeit ein (z.B. 3.5).")
        return
        
    if not current_recipe_inputs:
        messagebox.showwarning("Fehler", "Füge dem Rezept zuerst Zutaten hinzu!")
        return
        
    if output_id not in ITEMS:
        ITEMS[output_id] = {
            "name": output_name,
            "image": f"images/{output_id}.svg"
        }
        
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
    
    messagebox.showinfo("Erfolg", f"Rezept und Item für '{output_name}' erfolgreich gespeichert!")

# --- GUI LAYOUT ---
root = tk.Tk()
root.title("Foundry Rezept-Editor")
root.geometry("500x440")

frame_recipe = ttk.LabelFrame(root, text=" Rezept hinzufügen / bearbeiten ", padding=15)
frame_recipe.pack(fill="both", expand=True, padx=15, pady=15)

# Zeile 0: Ziel-Produkt Textfeld + NEUER LADEN BUTTON
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
combobox_recipe_type = ttk.Combobox(frame_recipe, values=["assembling", "smelting", "crushing"], state="readonly", width=12)
combobox_recipe_type.set("assembling")
combobox_recipe_type.grid(row=1, column=3, sticky="w", pady=5, padx=5)

# Trennlinie
ttk.Separator(frame_recipe, orient="horizontal").grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)

# Zeile 3: Zutaten hinzufügen
frame_ing_input = ttk.Frame(frame_recipe)
frame_ing_input.grid(row=3, column=0, columnspan=4, sticky="ew", pady=5)

ttk.Label(frame_ing_input, text="Zutat:").pack(side="left")
recipe_input_combobox = ttk.Combobox(frame_ing_input, state="readonly", width=18)
recipe_input_combobox.pack(side="left", padx=5)

ttk.Label(frame_ing_input, text="Anzahl:").pack(side="left")
entry_recipe_input_qty = ttk.Entry(frame_ing_input, width=5)
entry_recipe_input_qty.insert(0, "1")
entry_recipe_input_qty.pack(side="left", padx=5)

btn_add_ing = ttk.Button(frame_ing_input, text="+ Zutat", command=action_add_ingredient_to_list)
btn_add_ing.pack(side="left", padx=5)

# Zeile 4: Zutaten Liste
listbox_ingredients = tk.Listbox(frame_recipe, height=5)
listbox_ingredients.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=5)

btn_clear_ing = ttk.Button(frame_recipe, text="Leeren", command=action_clear_ingredients)
btn_clear_ing.grid(row=4, column=3, sticky="n", pady=5, padx=5)

# Zeile 5: Speichern Button
btn_save_recipe = ttk.Button(frame_recipe, text="Rezept dauerhaft speichern", command=action_add_recipe)
btn_save_recipe.grid(row=5, column=0, columnspan=4, sticky="ew", pady=15)

refresh_dropdowns()
root.mainloop()