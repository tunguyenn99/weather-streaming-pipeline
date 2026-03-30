# 🌀 Real-Time Weather Data Streaming Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge" alt="Maintained">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge" alt="PRs Welcome">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/Apache_Spark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white" alt="Spark">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
  <img src="https://img.shields.io/badge/uv-5D2DE2?style=for-the-badge&logo=python&logoColor=white" alt="uv">
</p>

A robust, end-to-end data engineering ecosystem for real-time weather analytics. This pipeline ingests live metrics from the **Open-Meteo API**, streams them through **Apache Kafka**, processes windowed aggregations with **PySpark**, and visualizes system performance via a **Prometheus & Grafana** monitoring stack.

-----

## 🏗️ System Architecture

The pipeline is built on a decoupled, event-driven architecture to ensure high availability and horizontal scalability:

![System Architecture](./excalidraw/weather_pipeline.png)

1.  **Data Ingestion:** Fetches live weather metrics (Temperature, Wind speed, etc.) from the **Open-Meteo API**.
2.  **Producer (Python):** A high-performance ingestion script managed by **uv** that polls the API and publishes JSON payloads to Kafka.
3.  **Message Broker (Kafka & Zookeeper):** Orchestrates high-throughput data buffering and decoupling between ingestion and processing.
4.  **Consumer (PySpark):** Leverages **Spark Structured Streaming** to ingest Kafka streams, enforce strict schemas, and calculate real-time windowed averages.
5.  **Monitoring Stack:**
      * **Kafka Exporter:** Scrapes internal Kafka metrics (offsets, partitions, broker info).
      * **Prometheus:** Serves as the time-series database for all system-level metrics.
      * **Grafana:** Provides real-time visualization of Kafka throughput and processing trends.

-----

## 🛠️ Tech Stack

  * **Language:** Python 3.11+ (Environment managed by **uv**)
  * **Streaming:** Apache Kafka, Zookeeper
  * **Processing:** Apache Spark (PySpark Structured Streaming)
  * **Monitoring:** Prometheus, Grafana, Kafka Exporter
  * **Infrastructure:** Docker, Docker Compose

-----

## 📂 Project Structure

```bash
.
├── producer/               # Python Producer (API -> Kafka)
│   ├── main.py             # Fetching & Publishing logic
│   └── Dockerfile
├── consumer/               # PySpark Consumer (Kafka -> Processing)
│   ├── main.py             # Structured Streaming & Aggregation logic
│   └── Dockerfile          # Spark image with Kafka connectors
├── monitoring/             # Monitoring Configuration
│   └── prometheus.yml      # Scrape configs for Kafka Exporter
├── grafana/                # Visualization
│   ├── dashboards/         # Pre-configured JSON dashboard exports
│   └── provisioning/       # Automated DataSource & Provider setup
├── docker-compose.yml      # Full stack orchestration
├── run_pipeline.sh         # Master startup script with auto-cleanup
├── pyproject.toml          # Dependency management (uv)
└── README.md
```

-----

## 🚀 Quick Start

### 1\. Prerequisites

Ensure you have **Docker** and **Docker Compose** installed. For local development, **uv** is recommended for high-speed dependency resolution.

### 2\. Launch the Pipeline

Use the provided master script to handle environment cleanup (clearing old Spark checkpoints) and service orchestration:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### 3\. Verify Operations

  * **Spark Aggregations:** Monitor real-time windowed outputs in your terminal:
    ```bash
    docker compose logs -f spark-consumer
    ```
  * **Kafka Health:** Verify topic health and data offsets:
    ```bash
    docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic weather_data
    ```

-----

## 📈 Monitoring & Visuals

The project includes a pre-configured Grafana dashboard that provides visibility into every stage of the pipeline:

### Kafka Performance Tracking
Monitor internal Kafka metrics such as broker status, message offsets, and partition distribution.
![Kafka Performance Tracking](./images/kafka/kafka_exporter.png)

### Data Ingestion Verification
Validate that the Python Producer is successfully fetching API data and sending JSON payloads to the Kafka broker.
![Data Ingestion Verification](./images/kafka/kafka_result.png)

### Prometheus Metric Exploration
Verify that the Kafka Exporter is being correctly scraped and check the raw time-series data for your topics.
![Prometheus Metric Exploration](./images/prometheus/execute_kafka_topic.png)

### End-to-End Dashboard
The final Grafana dashboard integrates all components for a holistic view of the system's health and data throughput.
![End-to-End Dashboard](./images/grafana/07_dashboard.png)

---

### 💡 Visual Setup Guide
If you are setting this up for the first time, you can refer to the step-by-step connection guides in the `images/grafana/` folder:
1. **Initialize Connection:** `01_connect_init.png`
2. **Connect Prometheus:** `02_connect_prometheus.png`
3. **Template Setup:** `05_kafka_exporter_template.png` (using ID 7589)

---

### 🤝 Connect & Community

* **Author**: [Tu Nguyen](https://www.linkedin.com/in/tunguyenn99/)
* **Community**: Join the [Xom Data](https://www.facebook.com/groups/xomdata/) community for more data analytics engineering insights!

*Built with ❤️ for the **Xom Data** community.*