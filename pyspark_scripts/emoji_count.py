from pyspark.sql.types import (
    ArrayType,
    StructType,
    StructField,
    StringType,
    IntegerType,
)
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
import pyspark.sql.functions as fn
import regex
import emoji
import re


def find_all_emo(plain_text):
    """
    Función find_all_emo soportada en librería emoji
    Argumentos: 
        plain_test (str): Texto que contiene los potenciales emojis
    Return: 
        emoji_list (List): Lista con el detalle de la ocurrencia del emoji
    """
    if plain_text is None:
        return None
    return emoji.emoji_list(plain_text)


if __name__ == "__main__":

    conf = SparkConf().setMaster("local[*]").setAppName("Dataframe_examples")
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    search_all_emojis = fn.udf(lambda y: find_all_emo(y), ArrayType(StringType()))

    df = spark.read.text("farmers-protest-tweets-2021-2-4.json")

    """
    El contenido del dataframe se puede analizar usando el get_json_object extrayendo el key .content
    para poder extraer los emojis disponibles se utilizar la libreria emoji y se aplica como una UDF esto retorna un 
    diccionario que contiene los diccionarios con el emoji y la posición donde se encontró.
    Resultados intermedios: 
    Col : emoji_in_post: [{'match_start': 85, 'match_end': 86, 'emoji': '🙄'}, {'match_start': 86, 'match_end': 87, 'emoji': '🙄'}]
    Col : emoji_in_post - explode step: convierte los elementos de la transformación anterior en filas, de esta forma que un solo diccionario por fila
          de esta manera se podrá avanzar en el conteo de cada emoji a tener ejemplo: 
          [{'match_start': 85, 'match_end': 86, 'emoji': '🙄'}, {'match_start': 86, 'match_end': 87, 'emoji': '🙄'}]
          row({'match_start': 85, 'match_end': 86, 'emoji': '🙄'})
          row({'match_start': 86, 'match_end': 87, 'emoji': '🙄'})
    Col : position - En esta transformación hacemos un substring para obtener el emoji, utilizamos específicamente un la terminación después del : 
    Col : Count - En esta transformación ya contamos el número de veces que un emoji aparece y ordenamos de mayor a menor

    """
    df = (
        df.select(fn.get_json_object(df.value, "$.content").alias("content"))
        .withColumn("emoji_in_post", search_all_emojis(fn.col("content"))) #[{'match_start': 85, 'match_end': 86, 'emoji': '🙄'}, {'match_start': 86, 'match_end': 87, 'emoji': '🙄'}]
        .select(explode("emoji_in_post").alias("emoji_in_post")) #row({'match_start': 86, 'match_end': 87, 'emoji': '🙄'})
        .withColumn('position', fn.expr('substr(emoji_in_post, locate("emoji", emoji_in_post)+6, 1 )')) #row({'match_start': 86, 'match_end': 87, 'emoji': '🙄'}) -> row('🙄')
        .groupBy(col('position')).count().orderBy(col("count").desc())
    )
