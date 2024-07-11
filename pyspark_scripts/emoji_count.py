from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as fn
import regex
import emoji
import re

df = spark.read.text("farmers-protest-tweets-2021-2-4.json")