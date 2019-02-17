## Summary


The project aims to analyze the execution times of various storage schemes - Avro, Parquet, and the default HBase format. Since Avro is row-storage and Parquet a columnar storage, the query execution times are analyzed on a variety of SQL queries like aggregation, range select, and selecting all rows.

Apache Hive is used as the querying engine. Since hive supports out of the box support for Avro, Parquet and HBase storage formats, there is a lesser overhead of setting up the querying infrastructure.

## Dataset

Public web-server logs were obtained from the NASA website. https://ita.ee.lbl.gov/html/traces.html
It has 3.7M log entries spanning over two months.


## High-level architecture of the data pipeline

![Data ingestion outline](https://github.com/saurabhmj/hive-project/blob/master/images/architecture.png)


Apache Hive is used for querying and analyzing the data from HBase and HDFS. Hive managed tables are created from data stored in HDFS in various formats such as ORC, Parquet & Avro.

## Data pre-processing

Even though publicly available, the log-entries were messy! Several of the entries had IP address errors, non-UTF characters, and uneven structuring of the URL. The data was pre-processed using a python script entry-by-entry and the script emitted the cleaned log entry. Though the current scheme emits one entry, the architecture can be extended to support multiple emits and multiple sources.


## Data ingestion

Apache Flume is used as an ingestion tool since it works well with data that streams and need to be sinked to multiple sources. The pipeline has one source which emits one log entry at a time and two sinks - HDFS and HBase table. The Flume source uses the console output of the pre-processing script and uses two channels: HDFSChannel and HBASEChannel, which as their names suggest ingest data into HDFS and HBase respectively. The configuration of flume is [here](https://github.com/saurabhmj/hive-project/blob/master/flume-conf.conf)

## Data Storage

Hive managed tables are employed to store data in ORC, Avro and Parquet data formats. The script to create all the tables is [here](https://github.com/saurabhmj/hive-project/blob/master/create_table.hql)


## Data Querying

Apache Hive is used as the querying engine. Queries were executed 5 times and a mean was calculated which is illustrated in the results below. The execution times of two Hive engines - MapReduce and Tez are compared to demonstrate the running efficiency of Tez Engine.

## Results

#### 1. Storage sizes of different file formats

![Storage sizes](https://github.com/saurabhmj/hive-project/blob/master/images/storage_sizes_graph.png)

HBase, as expected, takes up around 4 times more memory than the original file size. Since Avro, Parquet and ORC have the ability to compress the data, they take up lesser memory than the original size. 


#### 2. Data retrieval times for WHERE clause (random row access) 

```sql
SELECT COUNT(*) AS counts FROM server_logs_hbase 
WHERE status LIKE '2__';
```

![WHERE clause](https://github.com/saurabhmj/hive-project/blob/master/images/where_clause.png)

ORC and Parquet being columnar storage formats are faster than Avro, which would essentially need a full-scan. Furthermore, HBase and CSV are slower than Avro owing to the same reason of having to do the full scan.

#### 3. Data retrieval times for GROUP BY, ORDER BY clause (aggregation) 

```sql
SELECT domain_ext, COUNT(*) AS requests_per_domain FROM server_logs_hbase 
GROUP BY domain_ext 
ORDER BY requests_per_domain DESC;
```

![aggregation](https://github.com/saurabhmj/hive-project/blob/master/images/group_by_clause.png)

This query further illustrates the advantages of ORC and Parquet when the business query at hand has aggregation queries. There is a 3 times jump for the execution times of Parquet and HBase. One thing to note is that the HBase table has only one column family, which is very likely to the cause of the slow execution of aggregation, inspite of HBase being a column database.


#### 4. Data retrieval times for nested query

```sql
SELECT url, AVG(count_per_day) AS avg_per_day 
FROM  (SELECT date_format(server_ts,'D') AS day , url, COUNT(url) AS count_per_day 
      FROM server_logs_hbase 
      GROUP BY date_format(server_ts,'D'),url) t1 
GROUP BY day,url 
ORDER BY avg_per_day DESC 
LIMIT 15;
```

![nested](https://github.com/saurabhmj/hive-project/blob/master/images/nested_query.png)

Nested query execution times are very similar to those of aggregation and order by (3) with Parquet being 5 times faster than the HBase implementation.

## Observations, Challenges and work-arounds

* It was found that ORC and Parquet were extremely optimal storage formats, ORC being over 10 times more efficient than the actual size of the logs. The other benefit associated with column oriented stores like Parquet is that due to their inherent nature, executing aggregate-heavy queries on these data is also optimized, which outperforms querying results obtained by row oriented stores like Avro.

* **Apache Flume** on one hand is very flexible for helping data migrate, on the other hand requires a lot of configurations, many of which are empirical. Issues with configuring the capacity limit of channel (memory buffer) with source emission rate being very high compared to the sink (HDFS sink) write speed were worked around by keeping the source emission rates as minimal as possible. For HDFS sink, there are multiple parameters to vary such as rolling interval, rolling size, batch size that when tuned, perform exceptionally fast. Also, configuring HBase sink in Apache Flume is very restrictive. Flume provides serializers to get started but expects developers to implement custome serializers for their migration. This is where it truly shines as a tool and provides a useful decoupling framework.

