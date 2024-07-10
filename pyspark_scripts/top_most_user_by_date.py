from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("local[*]").setAppName("Dataframe_examples")
sc = SparkContext(conf=conf)

spark = SparkSession(sc)