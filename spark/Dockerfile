FROM bitnami/spark:3.5

USER root

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy Spark applications
COPY . /opt/spark-apps/

WORKDIR /opt/spark-apps

USER 1001
