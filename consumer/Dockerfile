FROM apache/spark:3.5.0

USER root
# Install Python and essential build tools
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Install uv (High-performance Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Force uv to install and use Python 3.11 for Spark compatibility
RUN uv python install 3.11
RUN uv sync --frozen --no-dev --group consumer

COPY consumer/main.py ./consumer/

# Set critical environment variables for PySpark
ENV JAVA_HOME=/opt/java/openjdk
ENV PYSPARK_PYTHON=/app/.venv/bin/python
ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages:$PYTHONPATH"

# Run the consumer application using the uv managed virtual environment
CMD ["uv", "run", "python", "consumer/main.py"]