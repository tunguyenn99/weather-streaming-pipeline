import json
import base64
import urllib.request
import os

def fetch_base64_logo(url):
    if not url: return None
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            b64 = base64.b64encode(data).decode('utf-8')
            mime = "image/svg+xml" if url.endswith(".svg") else "image/png"
            return f"data:{mime};base64,{b64}"
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return None

def main():
    nodes_config = [
        # Surround Wrapper
        {"id": "c1", "x": 40, "y": 40, "text": "WEATHER STREAMING ARCHITECTURE", "color": "#e03131", "bg": "#fff5f5", "is_container": True},
        
        # Data Flow (Row 1)
        {"id": "b1", "x": 100, "y": 160, "text": "Open-Meteo API", "color": "#1864ab", "bg": "#d0ebff", "logo": "https://cdn-icons-png.flaticon.com/512/4005/4005817.png", "phase": "SOURCE"},
        {"id": "b2", "x": 460, "y": 160, "text": "Python Producer", "color": "#2b8a3e", "bg": "#d3f9d8", "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg", "phase": "INGEST"},
        {"id": "b3", "x": 820, "y": 160, "text": "Kafka Broker", "color": "#e67700", "bg": "#fff3bf", "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachekafka/apachekafka-original.svg", "phase": "STREAM"},
        {"id": "b4", "x": 1180, "y": 160, "text": "Spark Consumer", "color": "#5f3dc4", "bg": "#e5dbff", "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachespark/apachespark-original.svg", "phase": "PROCESS"},
        
        # Monitoring (Row 2)
        {"id": "b5", "x": 820, "y": 420, "text": "Kafka Exporter", "color": "#c2255c", "bg": "#ffdeeb", "logo": "https://raw.githubusercontent.com/prometheus/prometheus/main/docs/prometheus-logo.png", "phase": "METRICS"},
        {"id": "b6", "x": 1180, "y": 420, "text": "Prometheus TSDB", "color": "#e8590c", "bg": "#ffe8cc", "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original.svg", "phase": "STORE"},
        {"id": "b7", "x": 1540, "y": 420, "text": "Grafana Dashboard", "color": "#1971c2", "bg": "#d0ebff", "logo": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/grafana/grafana-original.svg", "phase": "VISUALIZE"},
    ]

    elements = []
    files = {}

    for i, node in enumerate(nodes_config):
        nid, x, y = node["id"], node["x"], node["y"]
        is_container = node.get("is_container", False)
        box_w = 1800 if is_container else 320
        box_h = 520 if is_container else 100

        # PHASE TEXT (SOURCE, INGEST...) - To và rõ chữ
        if not is_container and node.get("phase"):
            elements.append({
                "type": "text", "x": x, "y": y - 50, "width": box_w, "text": node["phase"].upper(),
                "fontSize": 18, "fontFamily": 1, "textAlign": "center", "strokeColor": "#495057", "opacity": 80
            })

        # MAIN RECTANGLE
        elements.append({
            "type": "rectangle", "id": nid, "x": x, "y": y, "width": box_w, "height": box_h,
            "strokeColor": node["color"], "backgroundColor": node["bg"], "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "dashed" if is_container else "solid",
            "roughness": 0, "roundness": {"type": 3}
        })

        if not is_container:
            # LOGO (60x60)
            logo_url = node.get("logo")
            text_x_start = x + 25
            if logo_url:
                data_url = fetch_base64_logo(logo_url)
                if data_url:
                    fid = f"logo_{nid}"
                    files[fid] = {"id": fid, "dataURL": data_url, "mimeType": "image/png", "created": 1}
                    elements.append({
                        "type": "image", "x": x + 15, "y": y + 20, "width": 60, "height": 60,
                        "fileId": fid, "status": "saved"
                    })
                    text_x_start = x + 90

            # TOOL NAME TEXT
            elements.append({
                "type": "text", "x": text_x_start, "y": y + 35, "width": 210, "height": 30,
                "text": node["text"], "fontSize": 20, "fontFamily": 1, "textAlign": "left", 
                "verticalAlign": "middle", "strokeColor": "#000000"
            })
        else:
            # CONTAINER TEXT
            elements.append({
                "type": "text", "x": x + 25, "y": y + 20, "text": node["text"], 
                "fontSize": 26, "fontFamily": 1, "strokeColor": node["color"]
            })

    # ARROW FUNCTION
    def add_arrow(sx, sy, ex, ey, sid, eid, label=None):
        elements.append({
            "type": "arrow", "x": sx, "y": sy, "points": [[0,0], [ex-sx, ey-sy]],
            "strokeColor": "#343a40", "strokeWidth": 2, "endArrowhead": "arrow",
            "startBinding": {"elementId": sid}, "endBinding": {"elementId": eid}
        })
        if label:
            elements.append({
                "type": "text", "x": sx + (ex-sx)/2 - 35, "y": sy + (ey-sy)/2 - 25, 
                "text": label, "fontSize": 16, "fontFamily": 1, "strokeColor": "#495057"
            })

    # CONNECTIONS
    add_arrow(420, 210, 460, 210, "b1", "b2", "Fetch")
    add_arrow(780, 210, 820, 210, "b2", "b3", "Produce")
    add_arrow(1140, 210, 1180, 210, "b3", "b4", "Consume")
    add_arrow(980, 260, 980, 420, "b3", "b5", "Scrape")
    add_arrow(1140, 470, 1180, 470, "b5", "b6")
    add_arrow(1500, 470, 1540, 470, "b6", "b7")

    # EXPORT
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": elements, "files": files}
    os.makedirs("excalidraw", exist_ok=True)
    with open("excalidraw/weather_pipeline.excalidraw", "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    print("Success: Generated at excalidraw/weather_pipeline.excalidraw")

if __name__ == "__main__": main()