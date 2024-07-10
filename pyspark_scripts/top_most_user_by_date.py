import pyspark.sql.functions as F
from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import row_number
from pyspark.sql.functions import get_json_object

if __name__ == '__main__': 

    #Para las pruebas se usar local[*] así utiliza todos los threads de la máquina en ambiente productivo se usa YARN. 
    conf = SparkConf().setMaster("local[*]").setAppName("Dataframe_examples")
    sc = SparkContext(conf=conf)

    spark = SparkSession(sc)


    #Lectura del archivo que contiene los JSON 
    df = spark.read.text("farmers-protest-tweets-2021-2-4.json")
    
    """"
    Para el primer ejercicio nos interesa hacer parse de las fechas y el username dado que queremos conocer 
    la fecha con mayores trinos y el usuario que mas trino respectivamente
    """
    df = df.select(
                get_json_object(df.value,"$.user.username").alias("username"),
                get_json_object(df.value,"$.date").cast('date').alias("date"))\
                .createOrReplaceTempView("dates_users")