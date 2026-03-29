# 🌀 Real-Time Weather Data Streaming Pipeline

A robust, end-to-end data engineering ecosystem for real-time weather analytics. This pipeline ingests live metrics from the **Open-Meteo API**, streams them through **Apache Kafka**, processes windowed aggregations with **PySpark**, and visualizes system performance via a **Prometheus & Grafana** monitoring stack.

---

## 🏗️ System Architecture

1.  **Data Source:** Fetches live weather metrics (Temperature, Wind speed, etc.) from the **Open-Meteo API**.
2.  **Producer (Python):** A high-performance script managed by `uv` that polls the API and publishes JSON payloads to Kafka.
3.  **Message Broker (Kafka & Zookeeper):** Orchestrates high-throughput data buffering and decoupling between ingestion and processing.
4.  **Consumer (PySpark):** Leverages **Spark Structured Streaming** to ingest Kafka streams, apply strict schemas, and perform real-time windowed aggregations.
5.  **Monitoring Stack:**
    * **Kafka Exporter:** Scrapes internal Kafka metrics (offsets, partitions, broker info).
    * **Prometheus:** Serves as the time-series database for all system-level metrics.
    * **Grafana:** Provides real-time visualization of Kafka throughput and processing trends.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12+ (Optimized with **uv** package manager)
* **Streaming:** Apache Kafka, Zookeeper
* **Processing:** Apache Spark (PySpark Structured Streaming)
* **Monitoring:** Prometheus, Grafana, Kafka Exporter
* **Infrastructure:** Docker, Docker Compose

---

## 📂 Project Structure

```bash
.
├── producer/               # Python Producer (API -> Kafka)
│   ├── main.py             # Logic for fetching & publishing data
│   └── Dockerfile
├── consumer/               # PySpark Consumer (Kafka -> Processing)
│   ├── main.py             # Structured Streaming & Aggregation logic
│   └── Dockerfile          # Spark image with Kafka connectors
├── monitoring/             # Monitoring Configuration
│   └── prometheus.yml      # Scrape configs for Kafka Exporter
├── grafana/                # Visualization
│   └── dashboards/         # Pre-configured dashboard exports
├── docker-compose.yml      # Service orchestration (Zk, Kafka, Spark, Prom, Grafana)
├── pyproject.toml          # Project dependencies (managed by uv)
└── README.md
```

---

## 🚀 Quick Start

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd weather-streaming-pipeline
    ```

2.  **Spin up the infrastructure:**
    ```bash
    docker compose up -d
    ```

3.  **Verify the Pipeline:**
    * **Spark Logs:** Check real-time aggregations with `docker compose logs -f spark-consumer`.
    * **Grafana Dashboard:** Access `http://localhost:3000` (Default: `admin/admin`) to view Kafka performance.
    * **Prometheus:** Check metric health at `http://localhost:9090`.

---

## 📈 Monitoring Insights
The project includes a pre-configured Grafana dashboard that tracks:
* **Incoming Message Rate:** Real-time throughput from the weather API.
* **Topic Storage Size:** Total message count and partition health.
* **Spark Processing Logs:** Console-based output for windowed temperature averages.

---

**Note:** Ensure you have Docker and Docker Compose installed. This project uses `uv` for local development, but all services are fully containerized for seamless deployment.