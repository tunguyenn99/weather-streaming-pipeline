import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

def main():
    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("WeatherStreamingConsumer") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # 2. Schema
    schema = StructType([
        StructField("temperature", DoubleType()),
        StructField("windspeed", DoubleType()),
        StructField("winddirection", DoubleType()),
        StructField("weathercode", DoubleType()),
        StructField("time", StringType()),
        StructField("timestamp", DoubleType())
    ])

    # 3. Read from Kafka
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    topic = os.getenv("WEATHER_TOPIC", "weather_data")

    # THAY ĐỔI QUAN TRỌNG: Dùng "group.id" thay vì "kafka.group.id" và thêm enable.auto.commit
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic) \
        .option("group.id", "weather-consumer-group") \
        .option("kafka.group.id", "weather-consumer-group") \
        .option("startingOffsets", "earliest") \
        .load()

    # 4. Parse JSON
    weather_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("event_time", col("timestamp").cast(TimestampType()))

    # 5. Transformation
    avg_temp_df = weather_df \
        .withWatermark("event_time", "10 minutes") \
        .groupBy(window(col("event_time"), "5 minutes")) \
        .agg(avg("temperature").alias("average_temp"))

    # 6. Output to Console 
    query = avg_temp_df.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("checkpointLocation", "/tmp/checkpoints/weather_stats") \
        .trigger(processingTime='10 seconds') \
        .option("kafka.group.id", "weather-consumer-group") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()