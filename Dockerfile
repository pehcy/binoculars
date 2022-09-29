FROM ubuntu:22.04

# Install Java
RUN apt-get update \
 && apt-get install -y openjdk-11-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Spark
RUN apt-get update \
    && apt-get install -y curl \
    && curl https://archive.apache.org/dist/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz -o spark.tgz \
    && tar -xf spark.tgz \
    && mv spark-3.3.0-bin-hadoop3 /opt/spark/

# Set Spark environment
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin