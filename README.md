## Queries for creating hive tables:

1. flight_data_denorm:

```sql
CREATE TABLE flight_data_denorm (
  YEAR INT, 
  MONTH INT,
  DAY_OF_MONTH INT,
  FL_DATE DATE,
  UNIQUE_CARRIER STRING,
  AIRLINE_ID INT,
  CARRIER STRING,
  TAIL_NUM STRING,
  FL_NUM STRING,
  ORIGIN_AIRPORT_ID INT,
  ORIGIN_AIRPORT_SEQ_ID INT,
  ORIGIN STRING,
  DEST_AIRPORT_ID INT,
  DEST_AIRPORT_SEQ_ID INT,
  DEST STRING,
  DEP_DELAY DOUBLE,
  ARR_DELAY DOUBLE,
  CANCELLED DOUBLE,
  DIVERTED DOUBLE,
  DISTANCE DOUBLE,
  carrier_desc STRING,
  origin_dest_names array<STRING> 
)
 STORED AS ORC;
```

2. airport lookup

```sql
CREATE EXTERNAL TABLE airport_lookup ( 
code STRING,
description STRING ) 
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDE PROPERTIES ( "input.regex" = '\\"(.+)\\",\\"(.+)\\"' ) 
LOCATION '/user/root/flight_data/airports' tblproperties ("skip.header.line.count"="1");
```





3. carrier lookup

```sql
CREATE EXTERNAL TABLE carrier_lookup ( 
code STRING,
description STRING ) 
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDE PROPERTIES ( "input.regex" = '\\"(.+)\\",\\"(.+)\\"' ) 
LOCATION '/user/root/flight_data/carriers' tblproperties ("skip.header.line.count"="1");
```



## Summary of query results:

**(Since we were running short on the Azure credits, we have used data only for month=3)**

| Query | Result                                 |
|---------------|--------------------------------------------------|
| Which airport name has the highest average departure delay?      | North Bend/Coos Bay, OR: Southwest Oregon Regional   |
| Which carrier name had the highest sum of arrival delays on 3/14/2016?      | SkyWest Airlines Inc. (2003 - )| 
  
  
