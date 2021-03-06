# Building a data pipeline  
<img src="https://github.com/CraigGo/Portfolio/blob/master/Data%20Engineering/pipeline-overall.png" width="100%" height="100%">  
How to use Kafka and Spark containers to write messages to HDFS files for subsequent processing in analytics.  

Apache Kafka is used for creating real-time data pipelines. In this example, we simply substitute a .json file for the messages that would be flowing in real-time.

Apache Spark is an open-source distributed general-purpose cluster-computing framework commonly used in data science and for scaling up big data analytics.

HDFS (Hadoop Distributed File System) is the primary data storage system used by Hadoop applications. HDFS is a key part of the many Hadoop ecosystem technologies, as it provides a reliable means for managing pools of big data and supporting related big data analytics applications. Once data is stored in HDFS, it may be queried in SQL for analytics via Spark SQL, Presto etc.. or moved into other data analytics repositories as needed. The data is stored in parquet files for high performance columnar access in analytics.

Docker is also used to spin up the containers needed in the cloud for this infrastructure. Here is the docker .yml file for the containers:

https://github.com/CraigGo/Portfolio/blob/master/Data%20Engineering/docker-compose.yml

The example below will demonstrate the commands needed to build a data pipeline:
https://github.com/CraigGo/Portfolio/blob/master/Data%20Engineering/Spark-Kafka-HDFS.md

# Tracking User Activity 
This demonstrates tracking user activity. A docker cluster was built out a Lambda Architecture prototype. The Lambda Architecture consists of 1) a speed layer, 2) a batch layer, and a 3) a serving layer. This focuses on the internally facing components of the batch layer and the speed layer, both built using Parquet files to create a scale out SQL columnar data store on top of the Hadoop Distributed File System (HDFS).

A pyspark shell in a spark container was created and used the spark kafka API to read the messages from the kafka topic into a spark dataframe and explored the resulting schema and binary data. A new spark dataframe was created with the key and value slots converted to string and explored the resulting schema and json data as strings.

Additionally, a spark dataframes was written out in parquet format to hadoop hdfs and used spark SQL to impose schema on the dataframes and perform examples of simple queries againt the dataframes using spark SQL.

This project simulates event tracking at a game development company. The latest mobile game has two events we are interested in tracking: buy a sword & join guild... This assignment constructs the API server to catch two different events using flask, kafka, python, spark and Apache zookeeper to maintain configuration information and provide distributed synchronization.

https://github.com/CraigGo/Portfolio/blob/master/Data%20Engineering/User-Event-Tracking.md
