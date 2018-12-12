from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.functions import col
from pyspark.sql.functions import array
from pyspark.sql.functions import collect_list
from pyspark.sql.functions import concat_ws

conf = SparkConf()
sc = SparkContext(conf = conf)
hive_context = HiveContext(sc)


airlines = hive_context.table("flight.flight_data_orc2")
airports = hive_context.table("flight.airport_lookup")
carriers = hive_context.table("flight.carrier_lookup")

carrier_desc = "carrier_desc"
origin_desc = "origin_desc"
dest_desc = "dest_desc"

#we do not observe any duplicates on airport lookup
airports = airports.dropDuplicates(['code'])

#we group the carriers over code and create a list of all possible descriptions. Then, we concat the descriptions as a string with '||' as a separator 
carriers = carriers.groupBy("code").agg(collect_list(carriers.description).alias('new_desc')).select([col("code"),concat_ws(" || ", col("new_desc")).alias("description")])

air_car = airlines.join(carriers, airlines.carrier == carriers.code).select([a for a in airlines.columns] + [carriers.description.alias(carrier_desc)])

print "\n\n\n"
print air_car.head(1)

combined = air_car.join(airports, air_car.origin == airports.code)\
		.select([a for a in air_car.columns] + [airports.description.alias(origin_desc)])\
		.join(airports, air_car.dest == airports.code)\
		.select([a for a in air_car.columns] + [origin_desc] + [airports.description.alias(dest_desc)])

print "\n\n\n"
print combined.head(2)
print "\n\n\n"

combined = combined.where(combined.month == 3).where(combined.day_of_month == 14).groupBy("carrier_desc").sum("arr_delay").withColumnRenamed("sum(arr_delay)", "sum_arr_delay").sort(col("sum_arr_delay").desc()).limit(5)

combined.write.format("csv").save("file:///root/flight_data/query22.csv")
