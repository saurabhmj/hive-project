use flight;

CREATE EXTERNAL TABLE server_logs_hbase
(ROWKEY STRING,
bytes STRING,
domain_ext STRING,
host STRING,
isip STRING,
server_ts STRING,
status STRING,
type STRING,
url STRING)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' 
WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key,log_info:bytes,log_info:domain_ext, log_info:host, log_info:isip, log_info:server_ts, log_info:status,log_info:type,log_info:url") 
TBLPROPERTIES ("hbase.table.name" = "server_logs");

CREATE EXTERNAL TABLE IF NOT EXISTS server_logs_csv
(host STRING,
server_ts STRING,
type STRING,
url STRING,
status STRING,
bytes STRING,
isip STRING,
domain_ext STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/root/flight_data/flume_csv/';

CREATE TABLE IF NOT EXISTS server_logs_orc
(host STRING,
server_ts STRING,
type STRING,
url STRING,
status STRING,
bytes STRING,
isip STRING,
domain_ext STRING)
STORED AS ORC;

INSERT INTO TABLE server_logs_orc SELECT * FROM server_logs_csv;

CREATE TABLE server_logs_parquet 
(host STRING,
server_ts STRING,
type STRING,
url STRING,
status STRING,
bytes STRING,
isip STRING,
domain_ext STRING)
STORED AS PARQUET;

INSERT INTO TABLE server_logs_parquet SELECT * FROM server_logs_csv;

CREATE TABLE server_logs_avro 
(host STRING,
server_ts STRING,
type STRING,
url STRING,
status STRING,
bytes STRING,
isip STRING,
domain_ext STRING)
STORED AS AVRO;

INSERT INTO TABLE server_logs_avro SELECT * FROM server_logs_csv;