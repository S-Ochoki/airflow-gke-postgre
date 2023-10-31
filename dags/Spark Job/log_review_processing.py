
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import col, expr

input_path = "gs://wizeline_bootcamp_bucket/RAW/log_reviews.csv" 
output_path = "gs://wizeline_bootcamp_bucket/STAGE/log_reviews_transformed.csv" 


# Initialize a Spark session
spark = SparkSession.builder.appName("XMLLogProcessing").getOrCreate()

df = spark.read.csv(input_path, header=True, inferSchema=True)

df = df.withColumn("log", col("log").cast(StringType()))

# Parse the XML data
df = df.select(
    col("id_review").alias("log_id"),
    expr("xpath_string(log, '/reviewlog/log/logDate')").alias("log_date"),
    expr("xpath_string(log, '/reviewlog/log/device')").alias("device"),
    expr("xpath_string(log, '/reviewlog/log/os')").alias("os"),
    expr("xpath_string(log, '/reviewlog/log/location')").alias("location"),
    expr("xpath_string(log, '/reviewlog/log/ipAddress')").alias("ip"),
    expr("xpath_string(log, '/reviewlog/log/phoneNumber')").alias("phone_number")
)

df = df.coalesce(1)

# Save the processed data to a new CSV file in GCS
df.write.csv(output_path, header=True, mode="overwrite")

# Stop the Spark session
spark.stop()