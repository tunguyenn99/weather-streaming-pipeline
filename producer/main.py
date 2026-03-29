import os
import time
import json
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv
from loguru import logger

# 1. Load cấu hình
load_dotenv()
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("WEATHER_TOPIC", "weather_data")
LAT = os.getenv("LAT", "21.0285")
LON = os.getenv("LON", "105.8542")
INTERVAL = int(os.getenv("FETCH_INTERVAL_SECONDS", 60))

# 2. Khởi tạo Kafka Producer
# Lưu ý: value_serializer giúp tự động chuyển dict thành chuỗi JSON byte
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def fetch_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Chỉ lấy phần current_weather và thêm timestamp
        weather = data.get("current_weather", {})
        weather["timestamp"] = time.time()
        weather["location"] = {"lat": LAT, "lon": LON}
        
        return weather
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None

def main():
    logger.info("Starting Weather Producer...")
    while True:
        data = fetch_weather()
        if data:
            producer.send(TOPIC, value=data)
            logger.info(f"Sent to Kafka: {data['temperature']}°C at {data['time']}")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()