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
#select sum(arr_delay) as sa, carrier_desc from flight_data_denorm where month=3 and day_of_month=14 group by carrier_desc sort by sa desc limit 5;
#print combined.select(col("origin_dest_names").getItem(0)).head(3)

#combined.groupBy("ORIGIN_DESC").avg("DEP_DELAY").withColumnRenamed("avg(DEP_DELAY)", "avg_dep_delay").sort(col("avg_dep_delay").desc()).head(5)

combined = combined.where(combined.month == 3).where(combined.day_of_month == 14).groupBy("carrier_desc").sum("arr_delay").withColumnRenamed("sum(arr_delay)", "sum_arr_delay").sort(col("sum_arr_delay").desc()).limit(5)

combined.write.format("csv").save("file:///root/flight_data/query2.csv")


