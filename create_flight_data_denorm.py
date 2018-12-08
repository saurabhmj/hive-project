from pyspark import SparkConf, SparkContext
from pyspark.sql import HiveContext
from pyspark.sql.functions import col
from pyspark.sql.functions import array

conf = SparkConf() 
sc = SparkContext(conf = conf)
hive_context = HiveContext(sc) 


airlines = hive_context.table("flight.flight_data_orc2") 
airports = hive_context.table("flight.airport_lookup")
carriers = hive_context.table("flight.carrier_lookup")

carrier_desc = "carrier_desc" 
origin_desc = "origin_desc" 
dest_desc = "dest_desc"

airports = airports.dropDuplicates(['code'])
carriers = carriers.dropDuplicates(['code'])

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

combined = combined.withColumn("origin_dest_names", array(origin_desc, dest_desc)).drop(origin_desc).drop(dest_desc) 
combined = combined.toDF(*[a.lower() for a in combined.columns])

combined.registerTempTable("temp_table")
hive_context.sql("CREATE TABLE flight.flight_data_denorm STORED AS ORC AS SELECT * from temp_table")



