FROM apache/spark:3.5.0

USER root
# Cài đặt Python và các công cụ cần thiết
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Cài đặt uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Ép uv cài đặt đúng phiên bản Python 3.11
RUN uv python install 3.11
RUN uv sync --frozen --no-dev --group consumer

COPY consumer/main.py ./consumer/

# Thiết lập các biến môi trường quan trọng
ENV JAVA_HOME=/opt/java/openjdk
ENV PYSPARK_PYTHON=/app/.venv/bin/python
ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages:$PYTHONPATH"

CMD ["uv", "run", "python", "consumer/main.py"]