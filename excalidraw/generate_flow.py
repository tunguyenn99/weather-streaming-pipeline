import json
import uuid
import time
import os

def create_element(el_type, x, y, width=200, height=60, text="", stroke_color="#1e1e1e", fill_color="transparent"):
    element_id = str(uuid.uuid4())
    # Basic Excalidraw Schema
    element = {
        "id": element_id,
        "type": el_type,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "strokeColor": stroke_color,
        "backgroundColor": fill_color,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "roundness": {"type": 3},
        "seed": 12345,
        "version": 1,
        "versionNonce": int(time.time()),
        "isDeleted": False,
        "updated": int(time.time()),
        "link": None,
        "locked": False,
        "customText": text # Temporary storage for the loop
    }
    
    if el_type == "text":
        element.update({
            "text": text,
            "fontSize": 18,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
        })
    return element

def create_arrow(start_node, end_node):
    # Calculate coordinates to connect two boxes
    sx = start_node["x"] + start_node["width"]
    sy = start_node["y"] + start_node["height"] / 2
    ex = end_node["x"]
    ey = end_node["y"] + end_node["height"] / 2
    
    return {
        "id": str(uuid.uuid4()),
        "type": "arrow",
        "x": sx,
        "y": sy,
        "width": ex - sx,
        "height": ey - sy,
        "strokeColor": "#1e1e1e",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "points": [[0, 0], [ex - sx, ey - sy]],
        "startBinding": {"elementId": start_node["id"], "focus": 0, "gap": 5},
        "endBinding": {"elementId": end_node["id"], "focus": 0, "gap": 5},
        "endArrowhead": "arrow"
    }

# --- 1. Initialize Nodes (Boxes) ---
# Horizontal Axis: Data Pipeline
api = create_element("rectangle", 0, 100, text="Open-Meteo API", fill_color="#e7f5ff")
producer = create_element("rectangle", 300, 100, text="Python Producer", fill_color="#fff4e6")
kafka = create_element("rectangle", 600, 100, text="Kafka Broker", fill_color="#fab005")
spark = create_element("rectangle", 900, 100, text="Spark Consumer", fill_color="#eebefa")

# Vertical/Side Axis: Monitoring
exporter = create_element("rectangle", 600, 250, text="Kafka Exporter", fill_color="#ffdeeb")
prometheus = create_element("rectangle", 900, 250, text="Prometheus", fill_color="#ffe8cc")
grafana = create_element("rectangle", 1200, 250, text="Grafana Dashboard", fill_color="#d3f9d8")

rect_nodes = [api, producer, kafka, spark, exporter, prometheus, grafana]
elements = []

# --- 2. Create Text Labels for each Box ---
for n in rect_nodes:
    # Create text that overlays the box
    t = create_element("text", n["x"], n["y"], n["width"], n["height"], text=n["customText"])
    elements.extend([n, t])

# --- 3. Create Connection Arrows ---
elements.append(create_arrow(api, producer))
elements.append(create_arrow(producer, kafka))
elements.append(create_arrow(kafka, spark))
elements.append(create_arrow(kafka, exporter))
elements.append(create_arrow(exporter, prometheus))
elements.append(create_arrow(prometheus, grafana))

# --- 4. Export to the excalidraw/ folder ---
# This ensures the file is created in the same directory as the script
output_path = os.path.join(os.path.dirname(__file__), "weather_pipeline_flow.excalidraw")

data = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20},
    "files": {}
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"DONE! File generated at: {output_path}")