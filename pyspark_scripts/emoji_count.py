from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType
import pyspark.sql.functions as fn
import regex
import emoji
import re

def find_all_emo(plain_text):
  if plain_text is None:
    return None
  #emo_list = regex.findall(escape_list,plain_text)
  return emoji.emoji_list(plain_text)

if __name__ == '__main__': 

    search_all_emojis = fn.udf(lambda y: find_all_emo(y), ArrayType(StringType()))

    df = spark.read.text("farmers-protest-tweets-2021-2-4.json")

    """
    El contenido del dataframe se puede analizar usando el get_json_object extrayendo el key .content
    para poder extraer los emojis disponibles se utilizar la libreria emoji y se aplica como una UDF esto retorna un 
    diccionario que contiene los diccionarios con el emoji y la posición donde se encontró.
    Resultados intermedios: 
    Col : emoji_in_post: [{'match_start': 85, 'match_end': 86, 'emoji': '🙄'}, {'match_start': 86, 'match_end': 87, 'emoji': '🙄'}]
    """
    df = df.select(fn.get_json_object(df.value,"$.content").alias('content'))\
        .withColumn("emoji_in_post", search_all_emojis(fn.col("content")))