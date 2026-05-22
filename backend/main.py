import json
import os
import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

items = load_json("items.json")
recipes = load_json("recipes.json")
machines = load_json("machines.json")
belts = load_json("belts.json")
purity = load_json("purity.json")
miners = load_json("miners.json")

class Settings(BaseModel):
    assemblerLevel: str
    crusherLevel: str
    smelterLevel: str
    minerLevel: str
    beltLevel: str
    purity: str

class Target(BaseModel):
    item: str
    rate: float

class RequestData(BaseModel):
    targets: list[Target]
    settings: Settings

@app.get("/data")
def get_data():
    return {
        "items": items,
        "recipes": recipes,
        "machines": machines,
        "belts": belts,
        "purity": purity
    }

@app.post("/calculate")
def calculate(req: RequestData):
    nodes = []
    edges = []
    
    demands = {}  # item_id -> total_rate
    edges_map = {}  # (source_item, target_item) -> rate

    def add_demand(item_id, rate, parent_id=None):
        if rate <= 0:
            return
        demands[item_id] = demands.get(item_id, 0.0) + rate
        if parent_id:
            pair = (item_id, parent_id)
            edges_map[pair] = edges_map.get(pair, 0.0) + rate
        
        if item_id in recipes:
            recipe = recipes[item_id]
            m_type = recipe["type"]
            
            # Purity yield multiplier
            yield_mult = 1.0
            if m_type == "crushing":
                yield_mult = purity.get(req.settings.purity, {}).get("yield", 1.0)
                
            recipe_output = recipe["outputs"][item_id] * yield_mult
            recipes_per_minute = rate / recipe_output

            for in_item, in_qty in recipe["inputs"].items():
                in_rate = recipes_per_minute * in_qty
                add_demand(in_item, in_rate, item_id)

    # Sum target rates by item
    target_rates = {}
    for target in req.targets:
        if target.rate > 0:
            target_rates[target.item] = target_rates.get(target.item, 0.0) + target.rate

    # Process all targets for recursive demands
    for item_id, rate in target_rates.items():
        add_demand(item_id, rate)

    # Build Vis.js nodes
    for item_id, total_rate in demands.items():
        name = items.get(item_id, {}).get("name", item_id)
        image = items.get(item_id, {}).get("image", "")
        
        if item_id in recipes:
            recipe = recipes[item_id]
            m_type = recipe["type"]
            
            # Get machine level speed
            if m_type == "assembling":
                m_level = req.settings.assemblerLevel
                m_image = "images/assembler.svg"
                m_display = "Assembler"
            elif m_type == "smelting":
                m_level = req.settings.smelterLevel
                m_image = "images/smelter.svg"
                m_display = "Smelter"
            elif m_type == "crushing":
                m_level = req.settings.crusherLevel
                m_image = "images/crusher.svg"
                m_display = "Crusher"
            else:
                m_level = "1"
                m_image = "images/assembler.svg"
                m_display = "Maschine"
                
            speed = machines.get(m_type, {}).get(m_level, {}).get("speed", 1.0)
            
            yield_mult = 1.0
            if m_type == "crushing":
                yield_mult = purity.get(req.settings.purity, {}).get("yield", 1.0)
                
            recipe_output = recipe["outputs"][item_id] * yield_mult
            recipes_per_minute = total_rate / recipe_output
            
            machine_time = recipe["time"] / speed
            machines_needed = recipes_per_minute / (60 / machine_time)
            machines_needed_rounded = math.ceil(machines_needed)
            
            tooltip = f"{name}\n({m_type.capitalize()} Lvl {m_level})\n{machines_needed_rounded}x Maschinen\nGesamtbedarf: {total_rate:.1f}/min"
            node_label = f"{name}\n{machines_needed_rounded}x {m_display} Lvl {m_level}"
        else:
            # Raw resource extraction (Miner)
            m_level = req.settings.minerLevel
            m_image = "images/miner.svg"
            speed = miners.get(m_level, {}).get("speed", 1.0)
            miners_needed = math.ceil(total_rate / speed) if speed > 0 else 0
            tooltip = f"{name}\n(Miner Lvl {m_level})\n{miners_needed}x Miner\nBedarf: {total_rate:.1f}/min"
            node_label = f"{name}\n{miners_needed}x Miner Lvl {m_level}"
            machines_needed_rounded = miners_needed
            
        nodes.append({
            "id": item_id,
            "label": node_label, 
            "title": tooltip, 
            "image": image,
            "rate": total_rate,
            "machineCount": machines_needed_rounded,
            "isOutput": False
        })

        # If this item is a target, add a virtual output node to the far right
        if item_id in target_rates:
            out_rate = target_rates[item_id]
            out_node_id = f"output_{item_id}"
            out_tooltip = f"Ausgang: {name}\nAusgabe-Rate: {out_rate:.1f}/min"
            
            nodes.append({
                "id": out_node_id,
                "label": f"Output: {name}\n{out_rate:.1f}/min", # Text visible for output node
                "title": out_tooltip,
                "image": image, # Use the actual item image (like maisbot.svg) for output node!
                "rate": out_rate,
                "machineCount": 0,
                "isOutput": True
            })
            
            edges.append({
                "from": item_id,
                "to": out_node_id,
                "label": f"{out_rate:.1f}/min"
            })

    # Build Vis.js edges for internal flows
    for (src, dest), flow_rate in edges_map.items():
        edges.append({
            "from": src,
            "to": dest,
            "label": f"{flow_rate:.1f}/min"
        })

    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
