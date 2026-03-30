# 📖 Pipeline Operation Guide (Producer & Consumer)

This document provides detailed instructions on how to configure, run, and verify the two main components of the weather streaming system.

---

## 📡 1. Producer: Weather Data Ingestion
**Role:** Connects to the Open-Meteo API, fetches real-time weather data, and pushes it to a Kafka topic in JSON format.

### 🛠 Configuration & Setup
* **Environment:** Python 3.12 (Managed by `uv`).
* **Core Libraries:** `kafka-python-ng`, `requests`.
* **Key Files:** `producer/main.py`, `producer/Dockerfile`.

### 🚀 How to Run
1.  **Run via Docker (Recommended):**
    ```bash
    docker compose up -d producer
    ```
2.  **Run Locally (For Debugging):**
    ```bash
    cd producer
    uv venv && source .venv/bin/activate
    uv pip install -r requirements.txt
    python main.py
    ```

### 🔍 Activity Verification
* **Check Logs:** `docker compose logs -f producer`
* **Success Indicator:** Logs should display: `Sent weather data to Kafka: {"location": "Hanoi", "temp": 27.7...}`.
* **Verify via Kafka Broker:**
    ```bash
    docker exec -it weather-streaming-pipeline-kafka-1 /opt/kafka_2.13-2.8.1/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic weather_data --group weather-monitoring-group --from-beginning
    ```

---

## ⚙️ 2. Consumer: PySpark Structured Streaming
**Role:** Reads the data stream from Kafka, applies a schema, performs windowed aggregation (e.g., 5-minute sliding average), and outputs the results.

### 🛠 Configuration & Setup
* **Technology:** Apache Spark 3.5.0, PySpark.
* **Checkpointing:** State is saved at `/tmp/checkpoints/weather_stats` to ensure fault tolerance (Exactly-once semantics).

### ⚠️ Important Note: Consumer Group
By default, Spark manages offsets via Checkpoints. To make this consumer visible on the **Grafana Dashboard**, you **MUST** explicitly configure the Group ID in your code:
```python
.option("kafka.group.id", "weather-pyspark-group")
```

### 🚀 How to Run
1.  **Run via Docker:**
    ```bash
    docker compose up -d --build spark-consumer
    ```
    *Note: If you encounter an `Incomplete log file` error, delete the checkpoint folder before starting.*

### 🔍 Activity Verification
* **Check Logs:** `docker compose logs -f spark-consumer`
* **Success Indicator:** After 1–2 minutes (Batch 0), you should see the results table:
    ```text
    +--------------------+------------+
    |              window|average_temp|
    +--------------------+------------+
    |{2026-03-30 13:10...|        27.7|
    +--------------------+------------+
    ```

---

## 📈 3. Monitoring (Grafana Dashboard)

Once both the Producer and Consumer are running, you can monitor their interaction via Grafana.

### Key Metrics to Watch:
* **Producer Throughput:** The rate at which messages are sent from `producer/main.py`.
* **Consumer Lag:** The delta between the latest message in Kafka and the last message processed by Spark.
* **Consumer Group Status:** If the command `kafka-consumer-groups.sh --list` shows your group name, the Lag charts will function correctly.

---

## 🔄 4. System Reset Procedure
If data becomes inconsistent or you wish to restart the pipeline from scratch:
1.  **Stop everything:** `docker compose down`
2.  **Clear old state:** `rm -rf consumer/checkpoints/*`
3.  **Start Infrastructure:** `docker compose up -d zookeeper kafka prometheus grafana`
4.  **Start Producer first:** `docker compose up -d producer`
5.  **Start Consumer last:** `docker compose up -d spark-consumer`

---
- **Author:** @tunguyenn99
- **Project:** Weather Data Streaming Pipeline