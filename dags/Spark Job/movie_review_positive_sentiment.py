
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.sql.functions import when, lit, col, concat_ws
from datetime import datetime

# Initialize a Spark session
spark = SparkSession \
        .builder \
        .appName("MovieReviewsTransform") \
        .getOrCreate()

# Load the data from Google Cloud Storage
input_path = "gs://wizeline_bootcamp_bucket/RAW/movie_reviews.csv" 
output_path = "gs://wizeline_bootcamp_bucket/STAGE/classified_movie_reviews.csv" 

#Read data from csv file
df = spark.read.csv(input_path, header=True)

# Tokenize the review_str column
tokenizer = Tokenizer(inputCol="review_str", outputCol="review_token")
df = tokenizer.transform(df)


# Remove stop words (optional)
remover = StopWordsRemover(inputCol="review_token", outputCol="review_clean")
df = remover.transform(df)

# Assuming 'df' is the DataFrame with 'review_clean' as an array of strings
# Concatenate the array of strings into a single string with space as a separator
df = df.withColumn("review_clean_str", concat_ws(" ", col("review_clean")))

# Now you can check if the concatenated string contains "good"
df = df.withColumn("positive_review", when(col("review_clean_str").contains("good"), 1).otherwise(0))

# Add a timestamp column
df = df.withColumn("insert_date", lit(datetime.now()))

# Rename columns
df = df.withColumnRenamed("cid", "user_id").withColumnRenamed("id_review", "review_id")

df = df.coalesce(1)

df.select("user_id", "positive_review", "review_id").write.csv(output_path, header=True, mode="overwrite")

# Stop the Spark session
spark.stop()