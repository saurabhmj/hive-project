from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.functions import col
from pyspark.sql.functions import array

conf = SparkConf() 
sc = SparkContext(conf = conf)
hive_context = HiveContext(sc) 


combined = hive_context.table("flight.flight_data_denorm") 

carrier_desc = "carrier_desc" 
origin_desc = "origin_desc" 
dest_desc = "dest_desc"

#print combined.select(col("origin_dest_names").getItem(0)).head(3)

#combined.groupBy("ORIGIN_DESC").avg("DEP_DELAY").withColumnRenamed("avg(DEP_DELAY)", "avg_dep_delay").sort(col("avg_dep_delay").desc()).head(5)

combined = combined.groupBy(col("origin_dest_names").getItem(0)).avg("dep_delay").withColumnRenamed("avg(dep_delay)", "avg_dep_delay").sort(col("avg_dep_delay").desc()).limit(5)

combined.write.format("csv").save("file:///root/flight_data/query1.csv")


