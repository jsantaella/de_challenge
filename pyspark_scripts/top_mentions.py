from pyspark.sql.types import (
    ArrayType,
    StructType,
    StructField,
    StringType,
    IntegerType,
)
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark import SparkContext, SparkConf
import pyspark.sql.functions as fn
import regex
import re


if __name__ == "__main__":

    conf = SparkConf().setMaster("local[*]").setAppName("Dataframe_examples")
    sc = SparkContext(conf=conf)

    spark = SparkSession(sc)

    # Lectura del archivo de trinos en memoria de Spark

    df = spark.read.text("farmers-protest-tweets-2021-2-4.json")
