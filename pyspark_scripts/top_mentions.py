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

    #Esquema de ArrayType para los registros que contiene el mentionedUsers, de esta forma solo extraemos los username que interesan
    user_schema = ArrayType(
        StructType([
            StructField("username", StringType(), True),
        ])
    )

    """
    Inicio del procesamiento del dataset
    1. Se leen los archivos json y se extrae el key 'mentionedUsers' este contiene las menciones del objeto trino
    2. Se procesa el mentionedUsers y se convierte en listas de nombres de usuario
    """
    df = df.withColumn(
        "username_mentions", fn.get_json_object(df.value, "$.mentionedUsers")
    ).withColumn(
        "username_mentions_list", from_json(col("username_mentions"), user_schema)
    )

    """
    Se continuan las transformaciones...
    1. Se filtran aquellos que son nulos o trinos que no hacen mención a ningún otro usuario esto permite disminuir el tamaño del DF

    """

    df = (df.filter(df.username_mentions.isNotNull())
        )
