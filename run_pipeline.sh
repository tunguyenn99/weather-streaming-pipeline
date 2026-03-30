#!/bin/bash

# --- Color Configuration for Logs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}   WEATHER DATA STREAMING PIPELINE STARTUP    ${NC}"
echo -e "${GREEN}==============================================${NC}"

# 1. Clean up corrupted checkpoints (Fixes: Incomplete log file error)
echo -e "${YELLOW}[1/5] Cleaning up old streaming checkpoints...${NC}"
# Note: Ensure this path matches your docker-compose volume mapping
rm -rf ./consumer/checkpoints/*
echo -e "Checkpoints cleared."

# 2. Shut down existing containers
echo -e "${YELLOW}[2/5] Stopping any running services...${NC}"
docker compose down --remove-orphans

# 3. Start Infrastructure (Kafka, Prometheus, Grafana)
echo -e "${YELLOW}[3/5] Starting Infrastructure Services...${NC}"
docker compose up -d zookeeper kafka prometheus grafana kafka-exporter
echo -e "Waiting for Kafka to be ready (15s)..."
sleep 15

# 4. Start Weather Producer
echo -e "${YELLOW}[4/5] Starting Weather Producer...${NC}"
docker compose up -d --build producer

# 5. Start Spark Consumer
echo -e "${YELLOW}[5/5] Starting Spark Streaming Consumer...${NC}"
docker compose up -d --build spark-consumer

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}   PIPELINE IS NOW UP AND RUNNING!           ${NC}"
echo -e "${BLUE}   - Grafana: http://localhost:3000          ${NC}"
echo -e "${BLUE}   - Prometheus: http://localhost:9090       ${NC}"
echo -e "${BLUE}   - Kafka Exporter: http://localhost:9308   ${NC}"
echo -e "${GREEN}==============================================${NC}"

# --- Log Selection Menu ---
echo -e "${YELLOW}Which logs would you like to follow?${NC}"
echo -e "1) ${BLUE}Producer${NC} (Weather API Ingestion)"
echo -e "2) ${BLUE}Spark Consumer${NC} (Data Processing)"
echo -e "3) ${BLUE}Both${NC} (Combined logs)"
echo -e "4) ${BLUE}Exit${NC} (Keep pipeline running in background)"

read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo -e "${GREEN}Following Producer logs... (Ctrl+C to stop logs)${NC}"
        docker compose logs -f producer
        ;;
    2)
        echo -e "${GREEN}Following Spark Consumer logs... (Ctrl+C to stop logs)${NC}"
        docker compose logs -f spark-consumer
        ;;
    3)
        echo -e "${GREEN}Following combined logs... (Ctrl+C to stop logs)${NC}"
        docker compose logs -f producer spark-consumer
        ;;
    4)
        echo -e "${GREEN}Pipeline is running in background. Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Pipeline remains running in background.${NC}"
        ;;
esac